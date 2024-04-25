from .base import PluginBase
from diffusers import DPMSolverSinglestepScheduler, DPMSolverMultistepScheduler, EulerDiscreteScheduler, EulerAncestralDiscreteScheduler, UniPCMultistepScheduler

# https://huggingface.co/docs/diffusers/api/schedulers/overview
scheduler_alias = {
    'DPM++ 2M': (DPMSolverMultistepScheduler, {}),
    'DPM++ 2M Karras': (DPMSolverMultistepScheduler, dict(use_karras_sigmas=True)),
    'DPM++ 2M SDE': (DPMSolverMultistepScheduler, dict(algorithm_type="sde-dpmsolver++")),
    'DPM++ 2M SDE Karras': (DPMSolverMultistepScheduler, dict(algorithm_type="sde-dpmsolver++", use_karras_sigmas=True)),
    'DPM++ SDE': (DPMSolverSinglestepScheduler, {}),
    'DPM++ SDE Karras': (DPMSolverSinglestepScheduler, dict(use_karras_sigmas=True, lower_order_final=True)),
    'Euler': (EulerDiscreteScheduler, {}),
    'Euler a': (EulerAncestralDiscreteScheduler, {}),
    'UniPC': (UniPCMultistepScheduler, {}),
}

class PluginScheduler(PluginBase):

    def setup_args(self, parser):
        parser.add_argument("--scheduler", type=str, choices=scheduler_alias.keys())

    def setup_pipe(self):
        scheduler = self.ctx.args.scheduler
        if not scheduler:
            return

        (Scheduler, config) = scheduler_alias[scheduler]
        self.ctx.pipe.scheduler = Scheduler.from_config(self.ctx.pipe.scheduler.config, **config)

    def pre_pipe(self):
        if not 'scheduler' in self.ctx.pipe_opts_otg:
            return

        (Scheduler, config) = scheduler_alias[self.ctx.pipe_opts_otg.pop('scheduler', None)]
        self.ctx.pipe.scheduler = Scheduler.from_config(self.ctx.pipe.scheduler.config, **config)
