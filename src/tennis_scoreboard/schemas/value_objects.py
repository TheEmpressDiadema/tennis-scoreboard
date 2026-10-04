from typing import Self
from dataclasses import dataclass

@dataclass(frozen=True)
class SetScore:
    first_player_score: int = 0
    second_player_score: int = 0

@dataclass(frozen=True)
class Score:
    first_player_name: str
    second_player_name: str
    first_set: SetScore = SetScore()
    second_set: SetScore = SetScore()
    third_set: SetScore = SetScore()

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            first_player_name=data['first_player_name'],
            second_player_name=data['second_player_name'],
            first_set=SetScore(**data['first_set']),
            second_set=SetScore(**data['second_set']),
            third_set=SetScore(**data['third_set'])
        )