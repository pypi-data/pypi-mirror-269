from argparse import ArgumentParser
from .base import PluginBase

class PluginDPO(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--dpo', type=float)

    def setup_pipe(self):
        if not self.ctx.args.dpo:
            return

        self.ctx.pipe.load_lora_weights(
            'radames/sdxl-turbo-DPO-LoRA',
            adapter_name="dpo",
        )
        self.ctx.loras.append(("dpo", self.ctx.args.dpo))
