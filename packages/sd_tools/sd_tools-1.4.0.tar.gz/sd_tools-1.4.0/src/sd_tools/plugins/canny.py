import torch
from PIL import Image
import numpy as np
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
from .base import PluginBase
from .utils import resize_image

class PluginCanny(PluginBase):

    def setup_args(self, parser):
        group = parser.add_argument_group('Canny')
        group.add_argument("--canny", type=str, help="Canny Reference Image")
        group.add_argument("--canny-high", type=int, default=100, help="Canny High")
        group.add_argument("--canny-low", type=int, default=200, help="Canny Low")
        group.add_argument("--canny-cond-scale", type=float, default=0.8, help="Controlnet Conditioning Scale")

    def setup(self):
        args = self.ctx.args
        if not args.canny:
            return

        self.ctx.pipeline_opts_extra['controlnet'] = ControlNetModel.from_pretrained(
            "diffusers/controlnet-canny-sdxl-1.0",
            torch_dtype=torch.float16,
            variant='fp16',
            use_safetensors=True,
        )
        import cv2
        image = cv2.Canny(np.array(load_image(args.canny)), args.canny_low, args.canny_high)
        image = image[:, :, None]
        self.canny_image = Image.fromarray(np.concatenate([image, image, image], axis=2))
        if self.ctx.debug:
            self.canny_image.save('canny.png')
        self.ctx.pipeline = StableDiffusionXLControlNetPipeline

    def setup_pipe(self):
        if not self.ctx.args.canny:
            return

        pipe_opts = self.ctx.pipe_opts
        resized = resize_image(self.canny_image, pipe_opts.width, pipe_opts.height)
        pipe_opts.width = resized.width
        pipe_opts.height = resized.height
        self.ctx.pipe_opts.image = resized
        self.ctx.pipe_opts_extra['controlnet_conditioning_scale'] = self.ctx.args.canny_cond_scale
