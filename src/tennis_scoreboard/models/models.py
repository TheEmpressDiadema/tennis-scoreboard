import uuid

from sqlalchemy import String, ForeignKey, Uuid, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from typing import Annotated, Any


intpk = Annotated[int, mapped_column(primary_key=True)]


class BaseModel(DeclarativeBase):

    repr_count: int
    repr_cols: list[str]

    def __repr__(self) -> str:
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or i < self.repr_count:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"

class Player(BaseModel):

    __tablename__ = 'players'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    repr_cols_num = 2
    repr_cols = ["id", "name"]


class Match(BaseModel):

    __tablename__ = 'matches'

    id: Mapped[intpk]
    uid: Mapped[uuid.UUID] = mapped_column('uuid', Uuid, default=uuid.uuid4)
    first_player_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    second_player_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey('players.id', ondelete='CASCADE'), 
        nullable=True, 
        default=None
        )
    score: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    first_player: Mapped["Player"] = relationship(
        argument='Player',
        foreign_keys=[first_player_id]
    )
    second_player: Mapped["Player"] = relationship(
        argument='Player',
        foreign_keys=[second_player_id]
    )
    winner: Mapped["Player | None"] = relationship(
        argument='Player',
        foreign_keys=[winner_id]
    )

    repr_cols_num = 6
    repr_cols = ['id', 'uid', 'first_player_id', 'second_player_id', 'winner_id', 'score']