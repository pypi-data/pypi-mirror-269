import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Tuple, Callable, Dict, Any, Literal
from itertools import zip_longest
from dataclasses import dataclass
import html


def match(data, tuple_type):
    if not isinstance(data, (tuple, list)):
        return False
    if len(data) != len(tuple_type):
        return False
    if any((type(x) != tp for x, tp in zip_longest(data, tuple_type))):
        return False
    return True

@dataclass
class Request:
   body: Dict[str, Any] | None
   query: Dict[str, List[str]]
   path: str
   method: Literal['GET'] | Literal['POST']

class Server:

    handlers: List[Tuple[str, str, Callable]] = []

    def GET(self, path: str):
        def wrapper(handler): self.handlers.append(('GET', path, handler))
        return wrapper

    def POST(self, path: str):
        def wrapper(handler): self.handlers.append(('POST', path, handler))
        return wrapper

    def dispatch(self, req: BaseHTTPRequestHandler):
        parsed_url = urlparse(req.path)
        body = None
        if 'Content-Length' in req.headers:
            content_length = int(req.headers['Content-Length'])
            body = json.loads(req.rfile.read(content_length).decode('utf-8'))
        request = Request(body=body, query=parse_qs(parsed_url.query), path=parsed_url.path, method=req.command)
        handler = next((handler for method, path, handler in self.handlers if method == req.command and path == parsed_url.path), None)
        self.response(req, handler(request) if handler else None)

    def response(self, req: BaseHTTPRequestHandler, resp):
        if resp is None:
            req.send_response(404)
            return
        if type(resp) is str:
            req.send_response(200)
            req.wfile.write(str.encode('utf-8'))
            return
        if match(resp, (str, bytes)):
            content_type, body = resp
            req.send_response(200)
            req.send_header('Content-Type', content_type)
            req.end_headers()
            req.wfile.write(body)
            return

        req.send_response(500)
        req.send_header('Content-Type', 'text/html')
        req.end_headers()
        req.wfile.write(f"""<html>
            <div>{html.escape(str(type(resp)))}</div>
            {', '.join(map(lambda x: html.escape(str(type(x))), resp)) if isinstance(resp, (tuple, list)) else ''}
            </html>""".encode('utf-8'))

    def listen(self, interface: str):
        class Handler(BaseHTTPRequestHandler):
            def do_POST(req): self.dispatch(req)
            def do_GET(req): self.dispatch(req)
        host, port = interface.split(':') if ':' in interface else ('127.0.0.1', interface)
        server = HTTPServer((host, int(port)), Handler)
        server.serve_forever()
