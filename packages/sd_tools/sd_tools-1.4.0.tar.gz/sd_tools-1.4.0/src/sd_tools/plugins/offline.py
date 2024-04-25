from .base import PluginBase

class PluginOffline(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--offline", action='store_true', help="Offline Mode")

    def setup(self):
        self.ctx.offline = self.ctx.args.offline
        self.ctx.pipeline_opts.local_files_only = self.ctx.args.offline
        self.ctx.pipeline_opts.resume_download = not self.ctx.args.offline
