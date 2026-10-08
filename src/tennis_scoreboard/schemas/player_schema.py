from typing import Self
from dataclasses import dataclass, field

from tennis_scoreboard.models.models import Player

@dataclass(frozen=True)
class PlayerSchema:
    name: str

    id: int | None = field(default=None)

    @classmethod
    def from_sqlalchemy_model(cls, player: Player) -> Self:
        return cls(
            id=player.id,
            name=player.name
        )

    def to_sqlalchemy_model(self) -> Player:
        model = Player(name=self.name)
        if id != None:
            model = Player(
                id=self.id,
                name=self.name
            )
        return model