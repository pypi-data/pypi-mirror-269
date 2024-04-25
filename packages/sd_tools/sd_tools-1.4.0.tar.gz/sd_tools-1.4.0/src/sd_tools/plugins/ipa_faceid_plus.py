import torch
from argparse import ArgumentParser
from diffusers.utils import load_image
from diffusers import DDIMScheduler
from .base import PluginBase
from .utils import hf_download

class PluginIPAdaptorFaceIDPlus(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        group = parser.add_argument_group('IP-Adator FaceID Plus V2')
        group.add_argument("--ipa-faceid-plus", type=str, help="Reference Image")

    def setup(self):
        if not self.ctx.args.ipa_faceid_plus:
            return

        from insightface.app import FaceAnalysis
        from insightface.utils import face_align
        import cv2

        app = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CoreMLExecutionProvider', 'CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        image = cv2.imread(self.ctx.args.ipa_faceid_plus)
        faces = app.get(image)

        self.faceid_embeds = torch.from_numpy(faces[0].normed_embedding).unsqueeze(0)
        self.face_image = face_align.norm_crop(image, landmark=faces[0].kps, image_size=224)

    def setup_pipe(self):
        if not self.ctx.args.ipa_faceid_plus:
            return

        from .ip_adapter.ip_adapter_faceid import IPAdapterFaceIDPlusXL

        self.ctx.pipe.scheduler = DDIMScheduler(
            num_train_timesteps=1000,
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
            steps_offset=1,
        )

        self.ctx.pipe = IPAdapterFaceIDPlusXL(
            self.ctx.pipe,
            "laion/CLIP-ViT-H-14-laion2B-s32B-b79K",
            hf_download("h94/IP-Adapter-FaceID/ip-adapter-faceid-plusv2_sdxl.bin", offline=self.ctx.offline),
            self.ctx.device,
            torch_dtype=torch.float16
        )

        self.ctx.pipe_opts_extra['faceid_embeds'] = self.faceid_embeds
        self.ctx.pipe_opts_extra['num_samples'] = 1
        self.ctx.pipe_opts_extra['face_image'] = self.face_image
        self.ctx.pipe_opts_extra['shortcut'] = False
        self.ctx.pipe_opts_extra['s_scale'] = 1.0
