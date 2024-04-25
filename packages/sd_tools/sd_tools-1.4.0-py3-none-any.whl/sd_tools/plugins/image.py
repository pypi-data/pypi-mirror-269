from .base import PluginBase
from diffusers import AutoPipelineForImage2Image
from diffusers.utils import load_image

class PluginImage(PluginBase):

    def setup_args(self, parser):
        group = parser.add_argument_group('Image to Image')
        group.add_argument("--image", type=str, help="Image Prompt")
        group.add_argument("--strength", type=float, default=0.5, help="higher strength -> more creativity")

    def setup(self):
        if not self.ctx.args.image:
            return

        self.ctx.pipeline = AutoPipelineForImage2Image
        self.ctx.pipe_opts.image = load_image(self.ctx.args.image)
        self.ctx.pipe_opts_extra['strength'] = self.ctx.args.strength
