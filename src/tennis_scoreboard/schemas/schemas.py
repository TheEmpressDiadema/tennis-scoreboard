from uuid import UUID
from dataclasses import dataclass


@dataclass
class PlayerSchema:
    id: int
    name: str

@dataclass
class MatchSchema:

    id: int
    uuid: UUID
    first_player_id: int
    second_player_id: int
    winner_id: int | None
    score: list[dict[str, int]]