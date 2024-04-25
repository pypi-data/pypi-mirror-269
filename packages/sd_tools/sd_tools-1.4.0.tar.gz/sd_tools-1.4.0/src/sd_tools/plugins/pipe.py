from dataclasses import asdict
from .base import PluginBase

class PluginPipe(PluginBase):

    def setup_pipe(self):

        if self.ctx.debug:
            print(f"{self.ctx.pipeline} {self.ctx.model}")

        if self.ctx.model.endswith(".safetensors"):
            self.ctx.pipe = self.ctx.pipeline.from_single_file(
                self.ctx.model,
                **{**asdict(self.ctx.pipeline_opts), **self.ctx.pipeline_opts_extra}
            ).to(self.ctx.device)
        else:
            self.ctx.pipe = self.ctx.pipeline.from_pretrained(
                self.ctx.model,
                **{**asdict(self.ctx.pipeline_opts), **self.ctx.pipeline_opts_extra}
            ).to(self.ctx.device)
