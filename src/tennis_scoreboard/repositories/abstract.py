from uuid import UUID
from typing import Protocol
from abc import ABC

from sqlalchemy.orm import Session

from tennis_scoreboard.schemas.score import Score
from tennis_scoreboard.models.models import Player, Match


class BaseRepository(ABC):

    def __init__(self, session: Session):
        self._session = session

class PlayerRepository(Protocol):

    def get_by_id(self, id: int) -> Player: ...

    def get_by_name(self, name: str) -> Player: ...

    def add(self, name: str) -> Player: ...

class MatchRepository(Protocol):

    def get_all(self) -> list[Match]: ...

    def get_by_uuid(self, uuid: UUID) -> Match: ...

    def get_ended_player_matches(self, player_id: int) -> list[Match]: ...

    def add(self, actor: Player, opponent: Player) -> Match: ...

    def update(self, uuid: UUID, score: Score, winner_id: int | None = None) -> Match: ...
