import os

from typing import Any, Callable
from urllib.parse import parse_qs
from http import HTTPStatus
from wsgiref.types import InputStream

from tennis_scoreboard.app.router import Router
from tennis_scoreboard.views.renderer import Renderer
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse


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

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        query = environ.get('QUERY_STRING', '')
        body = {}
        params = self._parse_query(query)
        if method == 'POST':
            body = self._get_body(
                environ['wsgi.input'],
                environ['CONTENT_LENGTH'],
                environ['CONTENT_TYPE']
            )

        request = HttpRequest(
            method=method,
            path=path,
            params={k:v[0] for k,v in params.items()},
            body=body
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