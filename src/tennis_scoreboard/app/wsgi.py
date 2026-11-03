from typing import Any, Callable

from tennis_scoreboard.app.router import Router
from tennis_scoreboard.views.renderer import Renderer
from tennis_scoreboard.controllers.structures import HttpRequest


class WsgiApp:

    def __init__(self, router: Router, renderer: Renderer):
        self._router = router
        self._renderer = renderer

    def __call__(self, environ: dict[str, Any], start_response: Callable) -> list[bytes]:
        return [b'']