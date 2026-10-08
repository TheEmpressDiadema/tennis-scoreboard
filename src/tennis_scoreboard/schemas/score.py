from typing import Any, Self
from dataclasses import dataclass

@dataclass(frozen=True)
class PlayerScore:
    points: str = '0'
    sets: int = 0
    games: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            games=data['games'],
            sets=data['sets'],
            points=data['points']
        )

@dataclass(frozen=True)
class Score:
    first_player_score: PlayerScore = PlayerScore()
    second_player_score: PlayerScore = PlayerScore()

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            first_player_score=PlayerScore.from_dict(data['first_player_score']),
            second_player_score=PlayerScore.from_dict(data['second_player_score'])
        )