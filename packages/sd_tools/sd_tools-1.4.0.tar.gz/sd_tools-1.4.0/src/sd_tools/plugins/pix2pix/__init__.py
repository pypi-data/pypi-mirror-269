import os
import torch
from argparse import ArgumentParser
from PIL import Image
from torchvision import transforms
import torchvision.transforms.functional as F
from .pix2pix_turbo import Pix2Pix_Turbo
from ..utils import obj, to8
from ..base import PluginBase


class PluginSketchToImage(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        group = parser.add_argument_group("Sketch to Image")
        group.add_argument("--sketch", type=str, help='Path to sketch image')
        group.add_argument('--sketch-gamma', type=float, default=0.4, help='The sketch interpolation guidance amount')

    def setup_pipe(self):
        if not self.ctx.args.sketch:
            return

        if not os.path.exists(self.ctx.args.sketch):
            image = Image.new("RGB", (self.ctx.pipe_opts.width, self.ctx.pipe_opts.height), (255,255,255))
            image.save(self.ctx.args.sketch)
            input(f"Open {self.ctx.args.sketch}, draw, close image eidtor, then press Enter to continue ")

        model = Pix2Pix_Turbo('sketch_to_image_stochastic', device=self.ctx.device)

        def run(**kwargs):
            with torch.no_grad():
                image_t = F.to_tensor(to8(Image.open(self.ctx.args.sketch).convert('RGB'))) < 0.5
                c_t = image_t.unsqueeze(0).to(self.ctx.device).float()
                B, C, H, W = c_t.shape
                images = model(
                    c_t,
                    kwargs['prompt'],
                    deterministic=False,
                    r=self.ctx.args.sketch_gamma,
                    noise_map=torch.randn((1, 4, H // 8, W // 8), device=c_t.device),
                )

                return obj(images=[transforms.ToPILImage()(images[0].cpu() * 0.5 + 0.5)])

        self.ctx.pipe = run
