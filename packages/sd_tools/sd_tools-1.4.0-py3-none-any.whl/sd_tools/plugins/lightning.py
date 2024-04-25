from diffusers import EulerDiscreteScheduler
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from argparse import ArgumentParser, Namespace
from .base import PluginBase

def hf_download(fullname, offline=False):
    ns, project, filename = fullname.split('/', 2)
    return hf_hub_download(repo_id=f"{ns}/{project}", filename=filename, local_files_only=offline, resume_download=not offline)

class PluginLightning(PluginBase):

    def setup_args(self, parser: ArgumentParser):
        parser.add_argument('--lightning', type=float)

    def setup_pipe(self):
        if not self.ctx.args.lightning:
            return

        pipe = self.ctx.pipe
        steps = self.ctx.pipe_opts.num_inference_steps

        if steps == 1:
            pipe.unet.load_state_dict(
                load_file(
                    hf_download("ByteDance/SDXL-Lightning/sdxl_lightning_1step_unet_x0.safetensors", offline=self.ctx.offline),
                    device=self.ctx.device))
            pipe.scheduler = EulerDiscreteScheduler.from_config(
                pipe.scheduler.config,
                timestep_spacing="trailing",
                prediction_type="sample")
            self.ctx.pipe_opts.guidance_scale = 0

        if steps > 1:
            pipe.load_lora_weights(
                hf_download(f"ByteDance/SDXL-Lightning/sdxl_lightning_{steps}step_lora.safetensors", offline=self.ctx.offline),
                adapter_name="lightning")
            self.ctx.loras.append(("lightning", self.ctx.args.lightning))
            self.ctx.pipe_opts.guidance_scale = 0
            pipe.scheduler = EulerDiscreteScheduler.from_config(
                pipe.scheduler.config,
                timestep_spacing="trailing")
