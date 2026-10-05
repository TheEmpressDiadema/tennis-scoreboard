from uuid import UUID, uuid4
from dataclasses import asdict
from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    String, ForeignKey, Uuid, Dialect, 
    JSON, CheckConstraint, TypeDecorator
)
from tennis_scoreboard.schemas.value_objects import Score


intpk = Annotated[int, mapped_column(primary_key=True)]


class ScoreType(TypeDecorator):

    impl = JSON
    cache_ok = True

    def process_bind_param(self, value: Score | None, dialect: Dialect):
        if value is None:
            return None
        return asdict(value)

    def process_result_value(self, value: dict | None, dialect: Dialect):
        if value is None:
            return None
        return Score.from_dict(value)

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

    repr_count = 2
    repr_cols = ["id", "name"]


class Match(BaseModel):

    __tablename__ = 'matches'

    id: Mapped[intpk]
    uuid: Mapped[UUID] = mapped_column(Uuid, default=uuid4, unique=True)
    first_player_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    second_player_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    winner_id: Mapped[int | None] = mapped_column(
        ForeignKey('players.id', ondelete='CASCADE'), 
        nullable=True, 
        default=None
        )
    score: Mapped[Score] = mapped_column(ScoreType, nullable=False)

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

    repr_count = 6
    repr_cols = ['id', 'uuid', 'first_player_id', 'second_player_id', 'winner_id', 'score']

    __table_args__ = (
        CheckConstraint("first_player_id != second_player_id", name="check_fk_equal"),
    )