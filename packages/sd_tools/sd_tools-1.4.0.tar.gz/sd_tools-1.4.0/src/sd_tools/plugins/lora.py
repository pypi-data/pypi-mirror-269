import os
from argparse import ArgumentParser
from .base import PluginBase

class PluginLora(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument("--loras", type=str, nargs='+', help="Loras")

    def setup_pipe(self):
        if self.ctx.args.loras:
            for idx, lora in enumerate(self.ctx.args.loras):
                (file, weight) = lora.split(':') if ':' in lora else (lora, 1.0)
                name = f"lora{idx}"
                self.ctx.pipe.load_lora_weights(file, adapter_name=name)
                self.ctx.loras.append((name, float(weight)))

        pipe = self.ctx.pipe
        if len(self.ctx.loras) > 0:
            pipe.set_adapters([x[0] for x in self.ctx.loras], adapter_weights=[x[1] for x in self.ctx.loras])
