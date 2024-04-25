import os
from argparse import ArgumentParser
from diffusers import DDIMScheduler
from .base import PluginBase
from .utils import hf_download
from diffusers.utils import load_image


class PluginIPCompositionAdapter(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        group = parser.add_argument_group('IP Composition Adapter')
        group.add_argument("--ip-composition", type=str, help="Reference image")
        group.add_argument("--ip-composition-scale", type=float, default=0.6, help="IPAdapter scale")

    def setup(self):
        if not self.ctx.args.ip_composition:
            return

    def setup_pipe(self):
        if not self.ctx.args.ip_composition:
            return

        from .ip_adapter.ip_adapter import IPAdapterPlus

        self.ctx.pipe.scheduler = DDIMScheduler.from_config(self.ctx.pipe.scheduler.config)

        hf_download("h94/IP-Adapter/models/image_encoder/config.json", offline=self.ctx.offline)
        image_encoder_path = os.path.dirname(hf_download("h94/IP-Adapter/models/image_encoder/model.safetensors", offline=self.ctx.offline))

        self.ctx.pipe = IPAdapterPlus(
            self.ctx.pipe,
            image_encoder_path,
            hf_download("ostris/ip-composition-adapter/ip_plus_composition_sd15.safetensors"),
            self.ctx.device,
            num_tokens=16
        )

        self.ctx.pipe_opts_extra['pil_image'] = load_image(self.ctx.args.ip_composition)
        self.ctx.pipe_opts_extra['scale'] = self.ctx.args.ip_composition_scale
