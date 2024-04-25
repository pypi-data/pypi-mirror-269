import argparse
from argparse import RawTextHelpFormatter

from sd_tools.plugins.safetensor import PluginSafetensor

from .plugins.debug import PluginDebug
from .plugins.base import Context, PipeOptions, PipelineOptions
from .plugins.lightning import PluginLightning
from .plugins.hyper import PluginHyper
from .plugins.photo_maker import PluginPhotoMaker
from .plugins.cfg import PluginCFG
from .plugins.size import PluginSize
from .plugins.prompt import PluginPrompt
from .plugins.wrong import PluginWrong
from .plugins.modelXL import PluginModelXL
from .plugins.pipe import PluginPipe
from .plugins.inpainting import PluginInpainting
from .plugins.ip_composition_xl import PluginIPCompositionAdapterXL
from .plugins.tcd import PluginTCD
from .plugins.lcm import PluginLCM
from .plugins.dpo import PluginDPO
from .plugins.steps import PluginSteps
from .plugins.output import PluginOutput
from .plugins.lora import PluginLora
from .plugins.seed import PluginSeed
from .plugins.scheduler import PluginScheduler
from .plugins.res_adapter import PluginResAdaptor
from .plugins.image import PluginImage
from .plugins.device import PluginDevice
# from .plugins.ipa import PluginIPAdaptor
from .plugins.ipa_plus import PluginIPAdaptorPlus
# from .plugins.ipa_faceid import PluginIPAdaptorFaceID
from .plugins.ipa_faceid_plus import PluginIPAdaptorFaceIDPlus
from .plugins.instantid import PluginInstantID
from .plugins.canny import PluginCanny
from .plugins.pose import PluginPose
from .plugins.depth import PluginDepth
from .plugins.offline import PluginOffline
from .plugins.http import PluginHTTP
from .plugins.run import PluginRun

def main():
    parser = argparse.ArgumentParser(
        description="Stable Diffusion XL",
        usage="",
        formatter_class=RawTextHelpFormatter,
        epilog="""
Examples:

    %(prog)s 'locomotive comming, masterpiece'

    %(prog)s 'portrait of a man' --model Lykon/dreamshaper-xl-lightning --steps 6 --size 576x1024 --cfg 1.5

"""
    )

    ctx = Context(arch='SDXL')
    plugins = [
        PluginDebug(ctx),
        PluginPipe(ctx),
        PluginOffline(ctx),
        PluginSafetensor(ctx),
        PluginInpainting(ctx),
        PluginModelXL(ctx),
        PluginDevice(ctx),
        PluginSize(ctx),
        PluginCFG(ctx),
        PluginPrompt(ctx),
        PluginSteps(ctx),
        PluginSeed(ctx),
        PluginWrong(ctx),
        PluginDPO(ctx),
        PluginTCD(ctx),
        PluginLCM(ctx),
        PluginLightning(ctx),
        PluginHyper(ctx),
        PluginOutput(ctx),
        PluginCanny(ctx),
        PluginPose(ctx),
        PluginDepth(ctx),
        PluginPhotoMaker(ctx),
        # PluginIPAdaptor(ctx),
        PluginIPAdaptorPlus(ctx),
        # PluginIPAdaptorFaceID(ctx),
        PluginIPAdaptorFaceIDPlus(ctx),
        PluginInstantID(ctx),
        PluginIPCompositionAdapterXL(ctx),
        PluginResAdaptor(ctx),
        PluginImage(ctx),
        PluginScheduler(ctx),
        PluginLora(ctx),
        PluginHTTP(ctx),
        PluginRun(ctx),
    ]

    ctx.plugins = plugins

    for plugin in plugins:
        plugin.setup_args(parser)

    ctx.args = parser.parse_args()

    for plugin in plugins:
        plugin.setup()

    for plugin in plugins:
        plugin.setup_pipe()
