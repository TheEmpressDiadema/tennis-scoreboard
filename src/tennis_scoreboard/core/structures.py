from dataclasses import dataclass, field
from typing import Any


@dataclass
class HttpRequest:
    method: str
    path: str
    params: dict[str, Any]

    def __getitem__(self, key: str) -> Any:
        return self.params.get(key)


@dataclass
class HttpResponse:
    code: int
    answer: str
    headers: dict[str, str] = field(
        default_factory=lambda : (
            {
                "Content-type" : "application/json",
                "Access-Control-Allow-Origin" : "*",
                "Access-Control-Allow-Methods" : "GET, POST, PATCH, OPTIONS",
                "Access-Control-Allow-Headers" : "Content-Type"
            }
        )
    )