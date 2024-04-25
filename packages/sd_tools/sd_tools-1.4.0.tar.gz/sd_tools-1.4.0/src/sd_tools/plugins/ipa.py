from argparse import ArgumentParser
from .base import PluginBase
from diffusers.utils import load_image

class PluginIPAdaptor(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument("--ipa", type=str, nargs='+', help="IP-Adaptor")
        parser.add_argument("--ipa-scale", type=float, default=0.6, help="IP-Adaptor Scale")

    def setup_pipe(self):
        args = self.ctx.args
        if not args.ipa:
            return

        pipe = self.ctx.pipe
        pipe.load_ip_adapter("h94/IP-Adapter", subfolder="sdxl_models", weight_name="ip-adapter_sdxl.bin", resume_download=not self.ctx.offline)
        self.ctx.pipe_opts_extra['ip_adapter_image'] = load_image(args.ipa[0])
        pipe.set_ip_adapter_scale(args.ipa_scale)
