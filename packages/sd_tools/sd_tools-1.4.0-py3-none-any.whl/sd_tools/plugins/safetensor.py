import torch
from .base import PluginBase

class PluginSafetensor(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--no-fp16", action="store_true", default=False, help="No fp16 weights")
        parser.add_argument("--no-safetensor", action="store_true", default=False, help="No safetensor")

    def setup(self):
        self.ctx.pipeline_opts.torch_dtype = torch.float16
        if self.ctx.args.no_fp16:
            self.ctx.pipeline_opts.variant = None
        if self.ctx.args.no_safetensor:
            self.ctx.pipeline_opts.use_safetensors = False
