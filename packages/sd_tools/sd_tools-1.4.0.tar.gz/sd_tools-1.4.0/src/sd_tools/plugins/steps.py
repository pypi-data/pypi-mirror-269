from argparse import Namespace
from .base import PluginBase

class PluginSteps(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--steps", type=int, default=1, help="Steps 1-50")

    def setup_pipe(self):
        self.ctx.pipe_opts.num_inference_steps = self.ctx.args.steps

    def pre_pipe(self):
        if 'steps' in self.ctx.pipe_opts_otg:
            self.ctx.pipe_opts.num_inference_steps = int(self.ctx.pipe_opts_otg.pop('steps'))
