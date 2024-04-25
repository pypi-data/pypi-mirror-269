from .base import PluginBase

class PluginCFG(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--cfg", type=float, default=0)

    def setup_pipe(self):
        self.ctx.pipe_opts.guidance_scale = self.ctx.args.cfg

    def pre_pipe(self):
        if 'cfg' in self.ctx.pipe_opts_otg:
            self.ctx.pipe_opts.guidance_scale = float(self.ctx.pipe_opts_otg.pop('cfg'))
