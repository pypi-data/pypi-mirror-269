from .base import PluginBase

class PluginDebug(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--debug", "-d", action="store_true", default=False)

    def setup(self):
        self.ctx.debug = self.ctx.args.debug
