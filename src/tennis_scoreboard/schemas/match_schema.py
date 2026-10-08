from uuid import UUID
from typing import Self
from dataclasses import dataclass, field

from tennis_scoreboard.models.models import Match
from tennis_scoreboard.schemas.player_schema import PlayerSchema
from tennis_scoreboard.schemas.score import Score

@dataclass(frozen=True)
class MatchSchema:

    id: int 
    first_player: PlayerSchema
    second_player: PlayerSchema
    score: Score

    winner: PlayerSchema | None = field(default=None)
    uuid: UUID | None = field(default=None)

    @classmethod
    def from_sqlalchemy_model(cls, match: Match) -> Self:
        winner = None if match.winner is None else PlayerSchema.from_sqlalchemy_model(match.winner)
        return cls(
            id=match.id,
            uuid=match.uuid,
            first_player=PlayerSchema.from_sqlalchemy_model(match.first_player),
            second_player=PlayerSchema.from_sqlalchemy_model(match.second_player),
            winner=winner,
            score=match.score
        )