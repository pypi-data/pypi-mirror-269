from argparse import Namespace
from huggingface_hub import hf_hub_download
import os
import torch
from .base import PluginBase
from diffusers.models import ControlNetModel
from diffusers.utils import load_image
from .utils import resize_image, hf_download

class PluginInstantID(PluginBase):

    def setup_args(self, parser):
        group = parser.add_argument_group("Instant ID")
        group.add_argument("--instantid", type=str, help="Reference Image")
        group.add_argument("--instantid-cond-scale", type=float, default=1.0, help="ControlNet Conditioning Scale")
        group.add_argument("--instantid-ipa-scale", type=float, default=0.7, help="IP-Adaptor Scale")

    def setup(self):
        if not self.ctx.args.instantid:
            return

        from .pipeline_stable_diffusion_xl_instantid import StableDiffusionXLInstantIDPipeline
        ctrlnet_path = hf_download("InstantX/InstantID/ControlNetModel/config.json", offline=self.ctx.offline)
        hf_download("InstantX/InstantID/ControlNetModel/diffusion_pytorch_model.safetensors", offline=self.ctx.offline)

        self.ctx.pipeline_opts_extra['controlnet'] = [ControlNetModel.from_pretrained(
            os.path.dirname(ctrlnet_path),
            torch_dtype=torch.float32 if self.ctx.device == 'mps' else torch.float16,
        )]
        self.ctx.pipeline_opts.torch_dtype = torch.float32 if self.ctx.device == 'mps' else torch.float16
        self.ctx.pipeline = StableDiffusionXLInstantIDPipeline

    def setup_pipe(self):
        if not self.ctx.args.instantid:
            return

        from insightface.app import FaceAnalysis
        import cv2
        import numpy as np
        from .pipeline_stable_diffusion_xl_instantid import draw_kps

        app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        app.prepare(ctx_id=0, det_size=(640, 640))

        face_image = load_image(self.ctx.args.instantid)
        face_image = resize_image(face_image, self.ctx.pipe_opts.width, self.ctx.pipe_opts.height)
        face_info = app.get(cv2.cvtColor(np.array(face_image), cv2.COLOR_RGB2BGR))
        face_info = sorted(face_info, key=lambda x:(x['bbox'][2]-x['bbox'][0])*x['bbox'][3]-x['bbox'][1])[-1]  # only use the maximum face
        self.ctx.pipe_opts_extra['image_embeds'] = face_info['embedding']

        pose_image = draw_kps(face_image, face_info['kps'])
        if self.ctx.debug:
            pose_image.save('instantid-face.webp')
        resized = resize_image(pose_image, self.ctx.pipe_opts.width, self.ctx.pipe_opts.height)

        self.ctx.pipe_opts.image = [resized]
        self.ctx.pipe_opts.width = resized.width
        self.ctx.pipe_opts.height = resized.height
        self.ctx.pipe_opts_extra['controlnet_conditioning_scale'] = self.ctx.args.instantid_cond_scale
        self.ctx.pipe_opts_extra['ip_adapter_scale'] = self.ctx.args.instantid_ipa_scale

        self.ctx.pipe.load_ip_adapter_instantid(
            hf_download("InstantX/InstantID/ip-adapter.bin", offline=self.ctx.offline))
