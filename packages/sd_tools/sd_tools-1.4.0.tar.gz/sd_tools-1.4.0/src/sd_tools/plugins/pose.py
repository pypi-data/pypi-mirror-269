import torch
from argparse import ArgumentParser
from diffusers import StableDiffusionXLControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
from PIL import Image
from .base import PluginBase

def resize_image(image, width, height):
    width0, height0 = image.size

    fit_width = width0 / height0 > width / height

    new_width = width if fit_width else int(width0 * height / height0)
    new_height = height if not fit_width else int(height0 * width / width0)

    resized = image.resize((new_width // 8 * 8, new_height // 8 * 8))
    return resized

    new_image = Image.new("RGB", (width, height), (0, 0, 0))
    new_image.paste(resized, ((width - new_width) // 2, (height - new_height) // 2))

    return new_image

class PluginPose(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--pose', type=str)

    def setup(self):
        if not self.ctx.args.pose:
            return

        from controlnet_aux import OpenposeDetector
        self.openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
        self.ctx.pipeline_opts_extra['controlnet'] = ControlNetModel.from_pretrained(
            "thibaud/controlnet-openpose-sdxl-1.0",
            torch_dtype=torch.float16,
            resume_download=not self.ctx.offline,
        )
        self.ctx.pipeline = StableDiffusionXLControlNetPipeline

    def setup_pipe(self):
        if not self.ctx.args.pose:
            return

        openpose_image = self.openpose(load_image(self.ctx.args.pose))
        resized = resize_image(openpose_image, self.ctx.pipe_opts.width, self.ctx.pipe_opts.height)
        self.ctx.pipe_opts.image = resized
        self.ctx.pipe_opts.width = resized.width
        self.ctx.pipe_opts.height = resized.height
