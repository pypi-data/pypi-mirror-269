from dataclasses import dataclass, field
from os import PathLike
from typing import Protocol, List, Any, Tuple, Optional, Dict, Union, Literal
import torch
from PIL.Image import Image
from argparse import ArgumentParser, Namespace
from diffusers import StableDiffusionPipeline, DiffusionPipeline

@dataclass
class PipelineOptions:
    torch_dtype: torch.dtype = torch.float16
    variant: Optional[str] = 'fp16'
    resume_download: bool = True
    local_files_only: bool = False
    use_safetensors: bool = True

@dataclass
class PipeOptions:
    prompt: str = ''
    image: Optional[Image] | List[Image] = None
    negative_prompt: str = ''
    width: int = 512
    height: int = 512
    num_inference_steps: int = 4
    guidance_scale: float = 0
    num_images_per_prompt: int = 1
    eta: float = 0

class Pipeline(Protocol):
    @staticmethod
    def from_pretrained(pretrained_model_name_or_path: str | PathLike, **kwargs: PipelineOptions) -> Any:
        pass

@dataclass
class Context:
    arch: Union[Literal['SD'] , Literal['SDXL']]
    args: Namespace = Namespace()
    pipeline: Optional[Any] = None
    pipeline_opts: PipelineOptions = PipelineOptions()
    pipeline_opts_extra: dict = field(default_factory=dict)
    pipe: Optional[Any] = None
    pipe_opts: PipeOptions = PipeOptions()
    pipe_opts_extra: dict = field(default_factory=dict)
    pipe_opts_otg: dict = field(default_factory=dict)
    loras: List[Tuple[str, float]] = field(default_factory=list)
    model: str = ''
    seed: Optional[int] = None
    offline: bool = False
    device: str = 'cpu'
    debug: bool = False
    count: int = 1
    plugins: List[Any] = field(default_factory=list)

class PluginBase():

    ctx: Context

    def __init__(self, ctx: Context):
        self.ctx = ctx

    def setup_args(self, parser: ArgumentParser):
        pass

    def setup(self):
        pass

    def setup_pipe(self):
        pass

    def pre_pipe(self):
        pass

    def post_pipe(self, result: Any):
        pass
