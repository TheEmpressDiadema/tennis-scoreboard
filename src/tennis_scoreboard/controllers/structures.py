from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, Self

from tennis_scoreboard.views.views import BaseView


@dataclass(frozen=True)
class HttpRequest:

    method: str
    path: str
    params: dict[str, Any]
    body: dict[str, Any]

@dataclass(frozen=True)
class HttpResponse:

    view: BaseView | None = field(default=None)
    status: HTTPStatus = field(default=HTTPStatus.OK)
    headers: list[tuple[str, str]] = field(default_factory = lambda : [('Content-type', 'text/html')])
    body: bytes = b''

    @classmethod
    def redirect(cls, location: str) -> Self:
        return cls(
            status=HTTPStatus.SEE_OTHER,
            headers=[('Location', location), (('Content-type', 'text/html'))]
        )