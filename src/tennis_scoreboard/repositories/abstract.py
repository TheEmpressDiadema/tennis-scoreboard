from typing import Protocol
from typing import Any

from tennis_scoreboard.models.models import Player, Match

class PlayerRepository(Protocol):

    def get_by_id(self, id: int) -> Player: ...

    def add(self, name: str) -> Player: ...

class MatchRepository(Protocol):

    def get_all(self) -> list[Match]: ...

    def get_by_id(self, id: int) -> Match: ...

    def add(self, actor: Player, opponent: Player) -> Match: ...

    def update(self, id: int, score: dict[str, Any]) -> Match: ...
