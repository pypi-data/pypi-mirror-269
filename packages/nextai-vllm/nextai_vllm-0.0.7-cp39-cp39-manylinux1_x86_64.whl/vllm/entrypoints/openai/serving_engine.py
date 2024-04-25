import asyncio
import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, List, Optional, Union
import os
import tqdm
import boto3
from pathlib import Path
import requests
from huggingface_hub import snapshot_download

from pydantic import conint

from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.entrypoints.openai.protocol import (ChatCompletionRequest,
                                              CompletionRequest, ErrorResponse,
                                              LogProbs, ModelCard, ModelList,
                                              AppSettings,
                                              ModelPermission)
from vllm.logger import init_logger
from vllm.lora.request import LoRARequest
from vllm.sequence import Logprob
from vllm.transformers_utils.tokenizer import get_tokenizer

logger = init_logger(__name__)

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY", None)
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY", None)

def download_object_from_s3(s3, *, bucket, key, version_id=None, filename):

    kwargs = {"Bucket": bucket, "Key": key}

    if version_id is not None:
        kwargs["VersionId"] = version_id

    object_size = s3.head_object(**kwargs)["ContentLength"]

    if version_id is not None:
        ExtraArgs = {"VersionId": version_id}
    else:
        ExtraArgs = None
    with tqdm.tqdm(total=object_size, unit="B", unit_scale=True, desc=filename) as pbar:
        s3.download_file(
            Bucket=bucket,
            Key=key,
            ExtraArgs=ExtraArgs,
            Filename=filename,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )


@dataclass
class LoRA:
    name: str
    local_path: str


class OpenAIServing:

    def __init__(self,
                 engine: AsyncLLMEngine,
                 served_model: str,
                 lora_modules=Optional[List[LoRA]],
                 app_settings: AppSettings = None):
        self.engine = engine
        self.served_model = served_model
        self.app_settings = app_settings
        if lora_modules is None:
            self.lora_requests = []
        else:
            self.lora_requests = [
                LoRARequest(
                    lora_name=lora.name,
                    lora_int_id=i,
                    lora_local_path=lora.local_path,
                ) for i, lora in enumerate(lora_modules, start=1)
            ]

        self.max_model_len = 0
        self.tokenizer = None

        try:
            event_loop = asyncio.get_running_loop()
        except RuntimeError:
            event_loop = None

        if event_loop is not None and event_loop.is_running():
            # If the current is instanced by Ray Serve,
            # there is already a running event loop
            event_loop.create_task(self._post_init())
        else:
            # When using single vLLM without engine_use_ray
            asyncio.run(self._post_init())

    async def _post_init(self):
        engine_model_config = await self.engine.get_model_config()
        self.max_model_len = engine_model_config.max_model_len

        # A separate tokenizer to map token IDs to strings.
        self.tokenizer = get_tokenizer(
            engine_model_config.tokenizer,
            tokenizer_mode=engine_model_config.tokenizer_mode,
            trust_remote_code=engine_model_config.trust_remote_code,
            truncation_side="left")

    async def show_available_models(self) -> ModelList:
        """Show available models. Right now we only have one model."""
        model_cards = [
            ModelCard(id=self.served_model,
                      root=self.served_model,
                      permission=[ModelPermission()])
        ]
        lora_cards = [
            ModelCard(id=lora.lora_name,
                      root=self.served_model,
                      permission=[ModelPermission()])
            for lora in self.lora_requests
        ]
        model_cards.extend(lora_cards)
        return ModelList(data=model_cards)

    def _create_logprobs(
        self,
        token_ids: List[int],
        top_logprobs: Optional[List[Optional[Dict[int, Logprob]]]] = None,
        num_output_top_logprobs: Optional[int] = None,
        initial_text_offset: int = 0,
    ) -> LogProbs:
        """Create OpenAI-style logprobs."""
        logprobs = LogProbs()
        last_token_len = 0
        if num_output_top_logprobs:
            logprobs.top_logprobs = []
        for i, token_id in enumerate(token_ids):
            step_top_logprobs = top_logprobs[i]
            if step_top_logprobs is not None:
                token_logprob = step_top_logprobs[token_id].logprob
            else:
                token_logprob = None
            token = step_top_logprobs[token_id].decoded_token
            logprobs.tokens.append(token)
            logprobs.token_logprobs.append(token_logprob)
            if len(logprobs.text_offset) == 0:
                logprobs.text_offset.append(initial_text_offset)
            else:
                logprobs.text_offset.append(logprobs.text_offset[-1] +
                                            last_token_len)
            last_token_len = len(token)

            if num_output_top_logprobs:
                logprobs.top_logprobs.append({
                    p.decoded_token: p.logprob
                    for i, p in step_top_logprobs.items()
                } if step_top_logprobs else None)
        return logprobs

    def create_error_response(
            self,
            message: str,
            err_type: str = "BadRequestError",
            status_code: HTTPStatus = HTTPStatus.BAD_REQUEST) -> ErrorResponse:
        return ErrorResponse(message=message,
                             type=err_type,
                             code=status_code.value)

    def create_streaming_error_response(
            self,
            message: str,
            err_type: str = "BadRequestError",
            status_code: HTTPStatus = HTTPStatus.BAD_REQUEST) -> str:
        json_str = json.dumps({
            "error":
            self.create_error_response(message=message,
                                       err_type=err_type,
                                       status_code=status_code).model_dump()
        })
        return json_str

    async def _check_model(self, request, token: Optional[str] = None, adapter_type: Optional[str] = "ft") -> Optional[ErrorResponse]:
        if request.model == self.served_model:
            return
        if request.model in [lora.lora_name for lora in self.lora_requests]:
            return
        # Check for lora modules in s3
        if request.model.startswith("ft:") and adapter_type == "ft":
            _request = requests.get(f'{self.app_settings.auth_server}/models/{request.model}/', headers={
                'x-api-key': token
            })
            if _request.status_code == 200:
                _model = (_request.json())["response"]
                path = _model["path"]
                session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                fragments = list(filter(lambda x: x.__len__() != 0 and x != 's3:', path.split("/")))
                s3 = session.client("s3")
                bucket = fragments[0]
                adapter = fragments[-1]
                prefix = '/'.join(fragments[1:])
                objects = s3.list_objects_v2(Bucket=bucket, Prefix=f'{prefix}/')
                if objects['KeyCount'] == 0:
                    raise Exception("Adapter in S3 path looks empty. Are you sure if the s3 location is right ?")
                files = objects['Contents']
                if files.__len__() == 0:
                    raise Exception("S3 folder looks empty. Are you sure if the s3 location is right ?")
                path = f'{Path.home().__str__()}/.cache/nextai/hub/{adapter}'
                path_like = Path(Path.home(), ".cache", "nextai", "hub", adapter, "tmp")
                dir = os.path.dirname(path_like)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                for object in files:
                    key = object['Key']
                    if not key.endswith("/"):
                        destination_file_name = key.split("/")[-1]
                        destination = Path(Path.home(), ".cache", "nextai", "hub", adapter, destination_file_name)
                        print(destination_file_name, os.path.exists(destination.__str__().strip()))
                        if not os.path.exists(destination.__str__().strip()):
                            download_object_from_s3(s3, bucket=bucket, key=key, version_id=None, filename=destination.__str__())
                            pass
                        else:
                            print(f"File already exists. Skipping {destination_file_name}")
                # After all the files in the object have been pulled, append the lora request to the lora_modules, so that the `@func _maybe_get_lora` can access it during inference
                self.lora_requests.append(
                    LoRARequest(
                        lora_name=adapter,
                        lora_int_id=self.lora_requests.__len__() + 1,
                        lora_local_path=path
                    )
                )
                return
        elif adapter_type == "open":
            path = snapshot_download(repo_id=request.model)
            self.lora_requests.append(
                    LoRARequest(
                        lora_name=request.model,
                        lora_int_id=self.lora_requests.__len__() + 1,
                        lora_local_path=path
                    )
                )
            return
        return self.create_error_response(
            message=f"The model `{request.model}` does not exist.",
            err_type="NotFoundError",
            status_code=HTTPStatus.NOT_FOUND)

    def _maybe_get_lora(self, request) -> Optional[LoRARequest]:
        if request.model == self.served_model:
            return
        for lora in self.lora_requests:
            if request.model == lora.lora_name:
                return lora
        # if _check_model has been called earlier, this will be unreachable
        raise ValueError("The model `{request.model}` does not exist.")

    def _validate_prompt_and_tokenize(
            self,
            request: Union[ChatCompletionRequest, CompletionRequest],
            prompt: Optional[str] = None,
            prompt_ids: Optional[List[int]] = None,
            truncate_prompt_tokens: Optional[conint(ge=1)] = None
    ) -> List[int]:
        if not (prompt or prompt_ids):
            raise ValueError("Either prompt or prompt_ids should be provided.")
        if (prompt and prompt_ids):
            raise ValueError(
                "Only one of prompt or prompt_ids should be provided.")

        if prompt_ids is None:
            tokenizer_kwargs = {} if truncate_prompt_tokens is None else {
                "truncation": True,
                "max_length": truncate_prompt_tokens,
            }
            input_ids = self.tokenizer(prompt, **tokenizer_kwargs).input_ids
        elif truncate_prompt_tokens is not None:
            input_ids = prompt_ids[-truncate_prompt_tokens:]
        else:
            input_ids = prompt_ids

        token_num = len(input_ids)

        if request.max_tokens is None:
            request.max_tokens = self.max_model_len - token_num

        if token_num + request.max_tokens > self.max_model_len:
            raise ValueError(
                f"This model's maximum context length is "
                f"{self.max_model_len} tokens. However, you requested "
                f"{request.max_tokens + token_num} tokens "
                f"({token_num} in the messages, "
                f"{request.max_tokens} in the completion). "
                f"Please reduce the length of the messages or completion.", )
        else:
            return input_ids
