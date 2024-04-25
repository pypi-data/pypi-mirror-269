from argparse import Namespace
from .base import PluginBase

class PluginPrompt(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("prompt", type=str, help="Prompt")
        parser.add_argument("--negative-prompt", "--np", type=str, default="worst quality, low quality, blurry, inappropriate pose, deformed, extra limbs, bad posture, bad makeup, watermark, signature, caption, bad eye, open mouth", help="Negative Prompt")

    def setup_pipe(self):
        self.ctx.pipe_opts.prompt = self.ctx.args.prompt
        self.ctx.pipe_opts.negative_prompt = self.ctx.args.negative_prompt

    def pre_pipe(self):
        if 'prompt' in self.ctx.pipe_opts_otg:
            self.ctx.pipe_opts.prompt = self.ctx.pipe_opts_otg.pop('prompt').strip()
        if 'negative_prompt' in self.ctx.pipe_opts_otg:
            self.ctx.pipe_opts.negative_prompt = self.ctx.pipe_opts_otg.pop('negative_prompt').strip()
