from argparse import ArgumentParser
from .base import PluginBase

class PluginWrong(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--wrong', type=float)

    def setup_pipe(self):
        if not self.ctx.args.wrong:
            return

        self.ctx.pipe.load_lora_weights(
            'minimaxir/sdxl-wrong-lora',
            adapter_name="wrong",
        )
        self.ctx.loras.append(("wrong", self.ctx.args.wrong))
        self.ctx.pipe_opts.negative_prompt =  'wrong,' + self.ctx.pipe_opts.negative_prompt
