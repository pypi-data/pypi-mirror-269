import os
import torch
from argparse import ArgumentParser
from diffusers import DDIMScheduler
from .base import PluginBase
from .utils import hf_download

class PluginIPAdaptorFaceID(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument("--ipa-faceid", type=str, help="IP-Adator FaceID")

    def setup(self):
        if not self.ctx.args.ipa_faceid:
            return

        from insightface.app import FaceAnalysis
        import cv2

        app = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        faces = app.get(cv2.imread(self.ctx.args.ipa_faceid))

        self.faceid_embeds = torch.from_numpy(faces[0].normed_embedding).unsqueeze(0)

    def setup_pipe(self):
        if not self.ctx.args.ipa_faceid:
            return

        from .ip_adapter.ip_adapter_faceid import IPAdapterFaceIDXL

        self.ctx.pipe.scheduler = DDIMScheduler(
            num_train_timesteps=1000,
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
            steps_offset=1,
        )

        self.ctx.pipe = IPAdapterFaceIDXL(
            self.ctx.pipe,
            hf_download("h94/IP-Adapter-FaceID/ip-adapter-faceid_sdxl.bin", offline=self.ctx.offline),
            self.ctx.device,
            torch_dtype=torch.float16)

        self.ctx.pipe_opts_extra['faceid_embeds'] = self.faceid_embeds
        self.ctx.pipe_opts_extra['num_samples'] = 1
