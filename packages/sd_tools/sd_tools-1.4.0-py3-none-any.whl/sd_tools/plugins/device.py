from argparse import ArgumentParser
import torch
from .base import PluginBase

class PluginDevice(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        device = 'cpu'
        if torch.cuda.is_available():
            device = 'cuda'
        if torch.backends.mps.is_available():
            device = 'mps'
        parser.add_argument("--device", type=str, default=device)

    def setup(self):
        self.ctx.device = self.ctx.args.device
