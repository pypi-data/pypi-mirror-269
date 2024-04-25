from argparse import Namespace
import random
import torch
from .base import PluginBase

class PluginSeed(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--seed", type=int, help=f"Seed 0-{2 ** 63 - 1}")

    def pre_pipe(self):
        seed = random.randint(0, 2 ** 63 - 1) if self.ctx.args.seed is None else self.ctx.args.seed
        torch.manual_seed(seed)
        self.ctx.seed = seed
