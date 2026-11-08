from collections.abc import Callable
from dataclasses import dataclass

from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse


@dataclass(frozen=True)
class Route:

    method: str
    pattern: str
    handler: Callable

class Router:

    def __init__(self) -> None:
        self._routes: list[Route] = []

    def register_route(self, method: str, pattern: str, handler: Callable) -> None:
        route = Route(method, pattern, handler)
        if not route in self._routes:
            self._routes.append(
                Route(method.upper(), pattern, handler)
            )

    def get_handler(self, method: str, path: str) -> Callable[[HttpRequest], HttpResponse]:
        method_ = method.upper()

        for route in self._routes:
            if route.method == method_ and route.pattern == path:
                return route.handler

        raise LookupError