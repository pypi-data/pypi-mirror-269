from argparse import ArgumentParser
from diffusers import LCMScheduler
from .base import PluginBase

class PluginLCM(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--lcm', type=float)

    def setup_pipe(self):
        if not self.ctx.args.lcm:
            return

        pipe = self.ctx.pipe
        pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
        pipe.load_lora_weights(
            "latent-consistency/lcm-lora-sdv1-5" if self.ctx.arch == 'SD' else "latent-consistency/lcm-lora-sdxl",
            adapter_name="lcm")
        self.ctx.loras.append(("lcm", self.ctx.args.lcm))
