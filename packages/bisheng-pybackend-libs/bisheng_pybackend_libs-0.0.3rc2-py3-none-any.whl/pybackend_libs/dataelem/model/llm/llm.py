# flake8: noqa
import time
from typing import Dict, List, Literal, Optional, Union

import torch
from accelerate import (dispatch_model, infer_auto_device_map,
                        init_empty_weights)
from pydantic import BaseModel, Field
from transformers import (AutoConfig, AutoModel, AutoModelForCausalLM,
                          AutoTokenizer, LlamaTokenizer)
from transformers.generation.utils import GenerationConfig


def torch_gc(devices):
    if torch.cuda.is_available():
        for device_id in devices:
            with torch.cuda.device(f'cuda:{device_id}'):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()


def torch_seed(seed=1947):
    # Set the seeds for reproducibility
    torch.cuda.manual_seed(seed)
    torch.manual_seed(seed)


class BaseLLM(object):
    def __init__(self, **kwargs):
        pass

    def predict(self, kwargs):
        raise Exception('not implemented')

    def completion(self, kwargs):
        raise Exception('not implemented')

    def _load(self,
              pretrain_path,
              precision,
              devices,
              gpu_memory,
              use_auto_model=False,
              use_safetensors=False,
              auto_configure_device_map=None,
              use_dispatch=False,
              use_generate_config=True,
              use_llamatokenizer=False,
              **kwargs):

        torch_seed()

        memory_per_device = int(int(gpu_memory) / len(devices))
        memory = f'{memory_per_device}GiB'
        max_memory = {int(device_id): memory for device_id in devices}

        auto_model_cls = AutoModel if use_auto_model else AutoModelForCausalLM

        if not use_auto_model and use_generate_config:
            self.generation_config = GenerationConfig.from_pretrained(
                pretrain_path)

        if not use_llamatokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(pretrain_path,
                                                       use_fast=False,
                                                       trust_remote_code=True)
        else:
            self.tokenizer = LlamaTokenizer.from_pretrained(pretrain_path,
                                                        add_eos_token=False,
                                                        add_bos_token=False,
                                                        eos_token='<eod>',
                                                        use_fast=False,
                                                        trust_remote_code=True)
            self.tokenizer.add_tokens(['<sep>', '<pad>', '<mask>', '<predict>',
                                       '<FIM_SUFFIX>', '<FIM_PREFIX>',
                                       '<FIM_MIDDLE>','<commit_before>',
                                       '<commit_msg>','<commit_after>',
                                       '<jupyter_start>','<jupyter_text>',
                                       '<jupyter_code>','<jupyter_output>',
                                       '<empty_output>'], special_tokens=True)

        with init_empty_weights():
            config = AutoConfig.from_pretrained(pretrain_path,
                                                trust_remote_code=True)
            model = auto_model_cls.from_config(config,
                                               torch_dtype=torch.float16,
                                               trust_remote_code=True)

        model.tie_weights()
        no_split_modules = model._no_split_modules
        torch_dtype = torch.float16
        if auto_configure_device_map is None:
            device_map = infer_auto_device_map(
                model,
                max_memory=max_memory,
                no_split_module_classes=no_split_modules)
        elif auto_configure_device_map is True:
            device_map = 'auto'
            torch_dtype = 'auto'
        else:
            device_map = auto_configure_device_map(
                model,
                max_memory=max_memory,
                no_split_module_classes=no_split_modules)

        if use_dispatch:
            model = auto_model_cls.from_pretrained(
                pretrain_path,
                trust_remote_code=True,
                use_safetensors=use_safetensors,
                **kwargs).half()
            self.model = dispatch_model(model, device_map=device_map)
        else:
            self.model = auto_model_cls.from_pretrained(
                pretrain_path,
                device_map=device_map,
                torch_dtype=torch_dtype,
                trust_remote_code=True,
                use_safetensors=use_safetensors,
                **kwargs)

        self.model.eval()


class ChatMessage(BaseModel):
    role: Literal['user', 'assistant', 'system', 'function', 'observation']
    content: str
    function_call: Optional[Dict] = None
    tools: Optional[List[dict]] = None
    metadata: Optional[str] = None


class DeltaMessage(BaseModel):
    role: Optional[Literal['user',
                           'assistant',
                           'system',
                           'observation']] = None
    content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    functions: Optional[List[Dict]] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    do_sample: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal['stop', 'length', 'function_call']


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Literal['stop', 'length']]


class UsageInfo(BaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0


class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal['chat.completion', 'chat.completion.chunk']
    choices: List[Union[ChatCompletionResponseChoice,
                        ChatCompletionResponseStreamChoice]]
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    usage: UsageInfo = UsageInfo()


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False
    do_sample: Optional[bool] = False
    stop: Optional[Union[str, List[str]]] = None
    top_k: Optional[int] = None


class Choise(BaseModel):
    text: str
    index: int = 0
    logprobs: Optional[float] = None
    finish_reason: Optional[Literal['stop', 'length']] = 'stop'


class CompletionResponse(BaseModel):
    id: str = 'cmpl-elem-1024',
    object: str = 'text_completion'
    model: str
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    choices: List[Choise] = []
