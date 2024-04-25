from dataclasses import asdict
from prompt_toolkit import prompt
from .base import PluginBase
from .utils import remove_none
import re
from typing import Tuple, Dict
import traceback

def parse(text: str) -> Dict[str, str]:
    pattern = r"[a-z0-9._-]+\s*=\s*[a-z0-9._-]+"
    return dict(
        prompt = re.sub(pattern, '', text, flags=re.IGNORECASE),
        **{key: val for (key, val) in [re.split(r'\s*=\s*', x) for x in re.findall(pattern, text, flags=re.IGNORECASE)]}
    )

class PluginRun(PluginBase):

    def setup_args(self, parser):
        parser.add_argument('--count', default=1, type=int, help="How many images to generate")
        parser.add_argument('--interactive', '-i', action='store_true', help="Interactive Mode")

    def setup(self):
        self.ctx.count = self.ctx.args.count

    def run(self):

        if 'count' in self.ctx.pipe_opts_otg:
            self.ctx.count = int(self.ctx.pipe_opts_otg.pop('count'))

        for no in range(self.ctx.count):

            for plugin in self.ctx.plugins:
                plugin.pre_pipe()

            if len(self.ctx.pipe_opts_otg) > 0:
                print(f"Invalid option(s): {', '.join(self.ctx.pipe_opts_otg.keys())}")
                return

            kwargs = {**remove_none(asdict(self.ctx.pipe_opts)), **self.ctx.pipe_opts_extra}
            if self.ctx.debug:
                print(kwargs)

            try:
                result = self.ctx.pipe(**kwargs)
            except Exception as e:
                print(e)
                if self.ctx.debug:
                    traceback.print_exc()
                break

            for plugin in self.ctx.plugins:
                plugin.post_pipe(result)

    def setup_pipe(self):
        if not self.ctx.args.interactive:
            self.run()
            return

        while True:
            try:
                cmd = prompt('> ', default=self.ctx.pipe_opts.prompt, vi_mode=True, mouse_support=True)
            except EOFError:
                exit()
            except KeyboardInterrupt:
                exit()
            if cmd == ':quit':
                exit()
            self.ctx.pipe_opts_otg = parse(cmd)
            self.run()
