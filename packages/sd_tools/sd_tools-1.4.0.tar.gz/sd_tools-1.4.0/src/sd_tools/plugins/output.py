import os
from .base import PluginBase
from datetime import datetime

class PluginOutput(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--output", "-o", nargs='+', type=str, help="Output File Name")

    def setup(self):
        outputs = self.ctx.args.output or ["output/{seed}.webp"]
        self.outputs = []
        for output in outputs:
            output = os.path.join(output, "{seed}.webp") if '.' not in os.path.basename(output) else output
            if os.path.dirname(output):
                os.makedirs(os.path.dirname(output), exist_ok=True)
            self.outputs.append(output)

    def post_pipe(self, result):
        for output in self.outputs:
            result.images[0].save(output.format(
                size=f"{self.ctx.pipe_opts.width}x{self.ctx.pipe_opts.height}",
                cfg=self.ctx.pipe_opts.guidance_scale,
                time=int(datetime.now().timestamp() * 1000),
                seed=self.ctx.seed,
            ))
