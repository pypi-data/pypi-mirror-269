from diffusers import DDIMScheduler
from huggingface_hub import hf_hub_download
from argparse import ArgumentParser
from .base import PluginBase
from .utils import hf_download

class PluginHyper(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--hyper', type=float)

    def setup_pipe(self):
        if not self.ctx.args.hyper:
            return

        pipe = self.ctx.pipe
        steps = self.ctx.pipe_opts.num_inference_steps

        if steps > 1:
            pipe.load_lora_weights(
                hf_download(f"ByteDance/Hyper-SD/Hyper-SDXL-{steps}steps-lora.safetensors", offline=self.ctx.offline),
                adapter_name="hyper")
            self.ctx.loras.append(("hyper", self.ctx.args.hyper))
            self.ctx.pipe_opts.guidance_scale = 0
            pipe.scheduler = DDIMScheduler.from_config(
                pipe.scheduler.config,
                timestep_spacing="trailing")
