import io
from dataclasses import asdict
import pkg_resources

from ..base import PluginBase
from .http import Server

class PluginHTTP(PluginBase):

    def setup_args(self, parser):
        parser.add_argument('--listen', type=str, help='Start a HTTP Server')

    def setup_pipe(self):
        if not self.ctx.args.listen:
            return

        def gen(payload):
            self.ctx.pipe_opts_otg = payload
            for plugin in self.ctx.plugins:
                plugin.pre_pipe()
            image = self.ctx.pipe(**{**asdict(self.ctx.pipe_opts), **self.ctx.pipe_opts_extra}).images[0]
            img_io = io.BytesIO()
            image.save(img_io, 'PNG')
            img_io.seek(0)
            return 'image/png', img_io.getvalue()

        server = Server()

        @server.GET('/')
        def get(req):
            if not 'prompt' in req.query:
                return 'text/html', pkg_resources.resource_string('sd_tools', 'plugins/http/assets/index.html')
            params = {k: int(v[0]) if v[0].isdigit() else v[0] for k, v in req.query.items()}
            return gen(params)

        @server.GET('/index.js')
        def get_js(req):
            return 'text/javascript', pkg_resources.resource_string('sd_tools', 'plugins/http/assets/index.js')

        @server.GET('/index.css')
        def get_css(req):
            return 'text/css', pkg_resources.resource_string('sd_tools', 'plugins/http/assets/index.css')

        @server.POST('/')
        def post(req):
            return gen(req.body)

        interface = self.ctx.args.listen
        host, port = interface.split(':') if ':' in interface else ('127.0.0.1', interface)
        print(f"listening on http://{host}:{port}")
        server.listen(self.ctx.args.listen)
