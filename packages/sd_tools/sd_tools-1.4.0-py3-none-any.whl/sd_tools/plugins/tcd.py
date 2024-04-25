from argparse import ArgumentParser
from diffusers import TCDScheduler
from .base import PluginBase

class PluginTCD(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--tcd', type=float)

    def setup_pipe(self):
        if not self.ctx.args.tcd:
            return

        pipe = self.ctx.pipe
        pipe.scheduler = TCDScheduler.from_config(pipe.scheduler.config)
        pipe.load_lora_weights(
            'h1t/TCD-SDXL-LoRA',
            adapter_name="tcd",
        )
        self.ctx.loras.append(("tcd", self.ctx.args.tcd))
        self.ctx.pipe_opts.eta = 0.3
