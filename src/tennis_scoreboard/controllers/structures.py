from http import HTTPStatus
from typing import Any
from dataclasses import dataclass, field

from tennis_scoreboard.views.views import BaseView

@dataclass
class HttpRequest:

    method: str
    path: str
    params: dict[str, Any]
    body: dict[str, Any]

@dataclass
class HttpResponse:

    status: HTTPStatus = field(default=HTTPStatus.OK)
    headers: list[tuple[str, str]] = field(default_factory = lambda :[('Content-type', 'text/html')])
    view: BaseView = field(default_factory=BaseView)