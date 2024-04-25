import os
import torch
from argparse import ArgumentParser
from .base import PluginBase
from diffusers.utils import load_image
from diffusers import AutoPipelineForInpainting
from PIL import Image

class PluginInpainting(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        group = parser.add_argument_group("Inpainting")
        group.add_argument("--inpaint", type=str, help="Image to inpaint")
        group.add_argument("--inpaint-mask", type=str, help="Mask")
        group.add_argument("--inpaint-blur", type=float, help="Blur mask")
        group.add_argument("--inpaint-strength", type=float, default=0.99, help="Strength")

    def setup(self):
        if not self.ctx.args.inpaint:
            return

        if not os.path.exists(self.ctx.args.inpaint_mask):
            image = load_image(self.ctx.args.inpaint)
            alpha = image.convert('RGBA')
            alpha.putalpha(Image.new('L', alpha.size, 127))
            alpha.save(self.ctx.args.inpaint_mask)
            input(f"Open {self.ctx.args.inpaint_mask}, mark the area for inpainting, close image eidtor, then press Enter to continue ")

        self.ctx.pipeline = AutoPipelineForInpainting

        if self.ctx.arch == 'SD':
            self.ctx.model = 'runwayml/stable-diffusion-inpainting'
        if self.ctx.arch == 'SDXL':
            self.ctx.model = 'diffusers/stable-diffusion-xl-1.0-inpainting-0.1'

    def pre_pipe(self):
        if not self.ctx.args.inpaint:
            return

        image = load_image(self.ctx.args.inpaint).convert('RGB')
        self.ctx.pipe_opts.image = image
        self.ctx.pipe_opts.width = image.width
        self.ctx.pipe_opts.height = image.height

        mask = Image.open(self.ctx.args.inpaint_mask)
        if mask.mode == 'RGBA':
            pixels = mask.load()
            for y in range(mask.height):
                for x in range(mask.width):
                    r, g, b, a = pixels[x, y]
                    pixels[x, y] = (0, 0, 0, 255) if a != 255 or r+g+b == 0 else (255,255,255,255)
            if self.ctx.debug:
                mask.save(f"{self.ctx.args.inpaint_mask}-processed.webp")

        mask = mask.convert('RGB')

        if self.ctx.args.inpaint_blur:
            mask = self.ctx.pipe.mask_processor.blur(mask, blur_factor=self.ctx.args.inpaint_blur)


        self.ctx.pipe_opts_extra['mask_image'] = mask
        self.ctx.pipe_opts_extra['strength'] = self.ctx.args.inpaint_strength
