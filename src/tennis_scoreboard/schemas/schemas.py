from uuid import UUID
from typing import Self
from dataclasses import dataclass

from tennis_scoreboard.models.models import Player, Match
from tennis_scoreboard.schemas.value_objects import Score


@dataclass(frozen=True)
class PlayerSchema:
    id: int
    name: str

    @classmethod
    def from_sqlalchemy(cls, player: Player) -> Self:
        return cls(
            id=player.id,
            name=player.name
        )
        

@dataclass(frozen=True)
class MatchSchema:

    id: int
    uuid: UUID
    first_player: PlayerSchema
    second_player: PlayerSchema
    winner: PlayerSchema | None
    score: Score

    @classmethod
    def from_sqlalchemy(cls, match: Match) -> Self:
        winner = None if match.winner is None else PlayerSchema.from_sqlalchemy(match.winner)
        return cls(
            id=match.id,
            uuid=match.uuid,
            first_player=PlayerSchema.from_sqlalchemy(match.first_player),
            second_player=PlayerSchema.from_sqlalchemy(match.second_player),
            winner=winner,
            score=match.score
        )