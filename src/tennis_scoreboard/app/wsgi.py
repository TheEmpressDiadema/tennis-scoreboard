import os

from typing import Any, Callable
from urllib.parse import parse_qs, urlparse
from wsgiref.types import InputStream

from tennis_scoreboard.app.router import Router
from tennis_scoreboard.views.renderer import Renderer
from tennis_scoreboard.controllers.structures import HttpRequest


class WsgiApp:

    def __init__(self, router: Router, renderer: Renderer):
        self._router = router
        self._renderer = renderer
        self._cwd = os.getcwd()

    def _get_body(self, wsgi_input: InputStream, content_length: str, content_type: str) -> dict[str, Any]:
        length = int(content_length)
        raw = wsgi_input.read(length).decode('utf-8')

        if 'application/x-www-form-urlencoded' in content_type:
            body = {k : v[0] for k,v in parse_qs(raw).items()}
        else:
            body = {}

        return body

    def _parse_query(self, query: str) -> dict[str, Any]:
        return parse_qs(query)

    def _serve_static(self, path: str, start_response: Callable) -> list[bytes]:
        relative_path = path.removeprefix('/static/')
        file_path = os.path.realpath(os.path.join('frontend/static/', relative_path))

        if not os.path.isfile(file_path) or not os.path.exists(file_path):
            start_response('404 Not Found', [('Content-type', 'text/plain')])
            return [b'Not found']

        content_type = 'text/css'
        
        headers = [
            ('Content-type', content_type)
        ]
        start_response('200 OK', headers)
        with open(file_path, 'rb') as f:
            return [f.read()]

    def __call__(self, environ: dict[str, str], start_response: Callable) -> list[bytes]:
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        uri = environ.get('REQUEST_URI', '/')
        if path.startswith('/static'):
            return self._serve_static(path, start_response)

        parsed_uri = urlparse(uri)
        params = parse_qs(parsed_uri.query)

        request = HttpRequest(
            method=method,
            path=path,
            params={k:v[0] for k,v in params.items()},
            body={}
        )
        handler = self._router.get_handler(method, path)
        response = handler(request)
        start_response(
            f'{response.status.value} {response.status.phrase}', 
            response.headers
        )
        if response.view is not None:
            return [self._renderer.render(response.view)]
        else:
            return [b'']