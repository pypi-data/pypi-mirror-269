from .base import PluginBase
from diffusers import StableDiffusionXLPipeline

class PluginModelXL(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--model", type=str, help="Model")

    def setup(self):
        if self.ctx.args.model:
            self.ctx.model = self.ctx.args.model
        if not self.ctx.model:
            self.ctx.model = "stabilityai/sdxl-turbo"
        if not self.ctx.pipeline:
            self.ctx.pipeline = StableDiffusionXLPipeline
