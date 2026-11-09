import logging
from collections.abc import Callable
from http import HTTPStatus
from logging.handlers import RotatingFileHandler
from typing import Any
from urllib.parse import parse_qs
from wsgiref.types import InputStream

from tennis_scoreboard.app.router import Router
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse
from tennis_scoreboard.views.renderer import Renderer
from tennis_scoreboard.views.views import NotFoundView


class WsgiApp:

    def __init__(self, router: Router, renderer: Renderer):
        self._router = router
        self._renderer = renderer
        self._setup_logging()

    def _setup_logging(self) -> None:
        file_handler = RotatingFileHandler(
            'application.log',
            maxBytes=5*1024*1024,
            encoding='utf-8'
        )
        console_handler = logging.StreamHandler()
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    def _serve_static(self, path: str) -> HttpResponse:
        try:
            body = self._renderer.render_css(path)
        except (FileNotFoundError, IsADirectoryError):
            return HttpResponse(status=HTTPStatus.NOT_FOUND, view=NotFoundView())
        except:
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return HttpResponse(
            status=HTTPStatus.OK,
            headers=[
                ('Content-Type', 'text/css; charset=utf-8'),
                ('Content-Length', str(len(body))),
            ],
            body=body,
        )

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

    def _get_response(self, request: HttpRequest) -> HttpResponse:
        if request.path.startswith('/static/'):
            return self._serve_static(request.path)

        try:
            handler = self._router.get_handler(request.method, request.path)
        except LookupError:
            return HttpResponse(status=HTTPStatus.NOT_FOUND, view=NotFoundView())
        except:
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return handler(request)

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        request = self._parse_request(environ)
        self._logger.info(
            f'REQUEST: METHOD: "{request.method}"; PATH: "{request.path}"; BODY: {request.body}, PARAMS: {request.params}'
        )
        response = self._get_response(request)

        body = (
            self._renderer.render(response.view)
            if response.view is not None
            else response.body
        )

        if response.status == HTTPStatus.INTERNAL_SERVER_ERROR:
            self._logger.exception('UNHANDLED EXCEPTION')
        else:
            self._logger.info(f'RESPONSE: STATUS: "{response.status}", HEADERS: {response.headers}')

        start_response(
            f'{response.status.value} {response.status.phrase}',
            response.headers,
        )
        return [body]