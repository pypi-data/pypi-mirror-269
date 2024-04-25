from argparse import ArgumentParser
from diffusers import LCMScheduler
from .base import PluginBase

class PluginYOSO(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--yoso', type=float)

    def setup_pipe(self):
        if not self.ctx.args.yoso:
            return

        self.ctx.pipe.scheduler = LCMScheduler.from_config(self.ctx.pipe.scheduler.config)
        self.ctx.pipe.load_lora_weights(
            'Luo-Yihong/yoso_sd1.5_lora',
            adapter_name="yoso",
        )
        self.ctx.loras.append(("yoso", self.ctx.args.yoso))
