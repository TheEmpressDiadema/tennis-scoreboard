from typing import Any
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
    thrid_set: SetScore = SetScore()

    def as_dict(self) -> list[dict[str, Any]]:
        return [
            {
                self.first_player_name : self.first_set.first_player_score,
                self.second_player_name : self.first_set.second_player_score
            },
            {
                self.first_player_name : self.second_set.first_player_score,
                self.second_player_name : self.second_set.second_player_score
            },
            {   
                self.first_player_name : self.thrid_set.first_player_score,
                self.second_player_name : self.thrid_set.second_player_score
            }
        ]
