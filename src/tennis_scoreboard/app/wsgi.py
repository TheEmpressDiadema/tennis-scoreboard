from http import HTTPStatus
from typing import Any, Callable
from urllib.parse import parse_qs
from wsgiref.types import InputStream

from tennis_scoreboard.app.router import Router
from tennis_scoreboard.views.renderer import Renderer
from tennis_scoreboard.views.views import NotFoundView
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse


class WsgiApp:

    def __init__(self, router: Router, renderer: Renderer):
        self._router = router
        self._renderer = renderer

    def _parse_body(self, wsgi_input: InputStream, content_length: str, content_type: str) -> dict[str, Any]:
        length = int(content_length)
        raw = wsgi_input.read(length).decode('utf-8')
        body = {}

        if 'application/x-www-form-urlencoded' in content_type:
            body = {k : v[0] for k,v in parse_qs(raw).items()}

        return body

    def _parse_request(self, environ: dict[str, Any]) -> HttpRequest:
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        query = environ.get('QUERY_STRING', '')
        wsgi_input = environ.get('wsgi.input', '')
        content_length = environ.get('CONTENT_LENGTH', '0')
        content_type = environ.get('CONTENT_TYPE', '')
        body = self._parse_body(
            wsgi_input,
            content_length,
            content_type
        )
        params = {k:v[0] for k,v in parse_qs(query).items()}
        return HttpRequest(
            method=method,
            path=path,
            params=params,
            body=body
        )

    def _get_content(self, path: str, response: HttpResponse) -> list[bytes]:
        if response.view is not None:
            return [self._renderer.render(response.view)]
        else:
            if path.startswith('/static/'):
                return [self._renderer.render_css(path)]
            else:
                return [b'']

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        try:
            request = self._parse_request(environ)
            handler = self._router.get_handler(request.method, request.path)
            response = handler(request)
        except LookupError:
            response = HttpResponse(
                status=HTTPStatus.NOT_FOUND,
                view=NotFoundView()
            )
        start_response(
            f'{response.status.value} {response.status.phrase}', 
            response.headers
        )
        return self._get_content(request.path, response)