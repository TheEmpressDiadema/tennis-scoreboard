from typing import Protocol

from tennis_scoreboard.models.models import Player, Match

class PlayerRepository(Protocol):

    def get_by_id(self, id: int) -> Player: ...

    def add(self, name: str) -> Player: ...

class MatchRepository(Protocol):

    def get_all(self) -> list[Match]: ...

    def get(self) -> Match: ...

    def upsert(self) -> Match: ...
