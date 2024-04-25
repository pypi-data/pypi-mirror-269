import torch
from argparse import ArgumentParser
from diffusers.utils import load_image
from .base import PluginBase
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
from transformers import pipeline
from .utils import resize_image

class PluginDepth(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--depth', type=str)

    def setup(self):
        if not self.ctx.args.depth:
            return

        pipe = pipeline(task="depth-estimation", model="LiheYoung/depth-anything-small-hf")
        self.depth = pipe(load_image(self.ctx.args.depth))["depth"]

        self.ctx.pipeline_opts_extra['controlnet'] = ControlNetModel.from_pretrained(
            "diffusers/controlnet-depth-sdxl-1.0-small",
            torch_dtype=torch.float16,
            variant='fp16',
            use_safetensors=True,
            resume_download=not self.ctx.offline,
        )
        self.ctx.pipeline = StableDiffusionXLControlNetPipeline

    def setup_pipe(self):
        if not self.ctx.args.depth:
            return

        resized = resize_image(self.depth, self.ctx.pipe_opts.width, self.ctx.pipe_opts.height)
        self.ctx.pipe_opts.image = resized
        self.ctx.pipe_opts.width = resized.width
        self.ctx.pipe_opts.height = resized.height
