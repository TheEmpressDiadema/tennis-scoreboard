from uuid import UUID
from typing import Protocol, Any

from tennis_scoreboard.models.value_objects import Score
from tennis_scoreboard.models.models import Player, Match

class PlayerRepository(Protocol):

    def get_by_id(self, id: int) -> Player: ...

    def add(self, name: str) -> Player: ...

class MatchRepository(Protocol):

    def get_all(self) -> list[Match]: ...

    def get_by_uuid(self, uuid: UUID) -> Match: ...

    def add(self, actor: Player, opponent: Player) -> Match: ...

    def update(self, uuid: UUID, score: Score) -> Match: ...
