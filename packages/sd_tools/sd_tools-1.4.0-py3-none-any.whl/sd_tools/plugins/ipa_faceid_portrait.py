import torch
from argparse import ArgumentParser
from diffusers import DDIMScheduler, AutoencoderKL
from .base import PluginBase
from .utils import hf_download


class PluginIPAdaptorFaceIDPortrait(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        group = parser.add_argument_group('IP-Adapter FaceID Portrait')
        group.add_argument("--ipa-portrait", type=str, nargs='+', help="photos")

    def setup(self):
        if not self.ctx.args.ipa_portrait:
            return

        self.ctx.pipeline_opts_extra['vae'] = AutoencoderKL.from_pretrained(
            "stabilityai/sd-vae-ft-mse").to(dtype=torch.float16)

    def setup_pipe(self):
        if not self.ctx.args.ipa_portrait:
            return

        import cv2
        from insightface.app import FaceAnalysis
        from .ip_adapter.ip_adapter_faceid_separate import IPAdapterFaceID

        app = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        faceid_embeds = []
        for image in self.ctx.args.ipa_portrait:
            faces = app.get(cv2.imread(image))
            faceid_embeds.append(torch.from_numpy(faces[0].normed_embedding).unsqueeze(0).unsqueeze(0))
        faceid_embeds = torch.cat(faceid_embeds, dim=1)

        self.ctx.pipe.scheduler = DDIMScheduler(
            num_train_timesteps=1000,
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
            steps_offset=1,
        )

        self.ctx.pipe = IPAdapterFaceID(
            self.ctx.pipe,
            hf_download("h94/IP-Adapter-FaceID/ip-adapter-faceid-portrait_sd15.bin", offline=self.ctx.offline),
            self.ctx.device,
            num_tokens=16,
            n_cond=len(self.ctx.args.ipa_portrait))

        self.ctx.pipe_opts_extra['faceid_embeds'] = faceid_embeds
