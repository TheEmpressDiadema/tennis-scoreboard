from dataclasses import asdict
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    Dialect,
    ForeignKey,
    String,
    TypeDecorator,
    Uuid,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)

from tennis_scoreboard.errors.validation_errors import (
    SamePlayersInputError,
    SymbolCountError,
    TooLongNameError,
    TooShortNameError,
    UndefinedSymbolError,
)
from tennis_scoreboard.schemas.score import Score

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

    def _validate_symbol_count(self, value: str, symbol: str) -> None:
        if value.count(symbol) > 2:
            symbol = '" "' if symbol == ' ' else symbol 
            raise SymbolCountError(f'Player name should have less then 3 {symbol}')

    def _validate_unexpected(self, value: str) -> None:
        unexpected_symbols = ".,/\\'#!\"$%^&*()0123456789+"
        for symbol in value:
            if symbol in unexpected_symbols:
                raise UndefinedSymbolError(f"Player name should not have symbols like '{unexpected_symbols}'")

    def _validate_length(self, value: str) -> None:
        if len(value) < 3:
            raise TooShortNameError('Player name length should be from 3 to 30 symbols')    
        if len(value) > 30:
            raise TooLongNameError('Player name length should be from 3 to 30 symbols')

    @validates('name')
    def validate_name(self, key: str, value: str):  
        self._validate_length(value)
        self._validate_unexpected(value)
        self._validate_symbol_count(value, '-')
        self._validate_symbol_count(value, ' ')
        return value

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

    @validates('second_player_id')
    def validate_equal_players(self, key: str, value: int) -> int:
        
        if value == self.first_player_id:
            raise SamePlayersInputError("Match contenders can't have same names")
        
        return value