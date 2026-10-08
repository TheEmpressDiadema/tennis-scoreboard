import pytest

from uuid import UUID
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert

from tests.utils import get_engine
from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.models.models import (
    BaseModel,
    Player,
    Match
)

def _fill_player(session_factory: sessionmaker[Session]) -> None:
    players = [
        Player(name='Victor'),
        Player(name='Dmitriy'),
        Player(name='Egor')
    ]

    with session_factory() as session:
        for player in players:
            stmt = insert(Player).values({"name" : player.name})
            session.execute(stmt)
        session.commit()
            

def _fill_matches(session_factory: sessionmaker[Session]) -> None:
    matches = [
        Match(
            uuid=UUID(hex='00000000-0000-0000-0000-000000000001'),
            first_player_id=1,
            second_player_id=2,
            score=Score()
            ),
        Match(
            uuid=UUID(hex='00000000-0000-0000-0000-000000000002'),
            first_player_id=2,
            second_player_id=3,
            score=Score()
        ),
        Match (
            uuid=UUID(hex='00000000-0000-0000-0000-000000000003'),
            first_player_id=1,
            second_player_id=2,
            winner_id=2,
            score=Score(
                first_player_score=PlayerScore(
                    games=2
                ),
                second_player_score=PlayerScore(
                    games=1
                )
            )
        )
    ]
    with session_factory() as session:
        session.add_all(matches)
        session.commit()

def _fill_table(engine: Engine, model: type[BaseModel]) -> None:
    session_maker = sessionmaker(engine)

    if model == Player:
        _fill_player(session_maker)
    if model == Match:
        _fill_matches(session_maker)

@pytest.fixture(scope='package', autouse=True)
def prepare_database() -> None:
    engine = get_engine()
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    
    _fill_table(engine, Player)
    _fill_table(engine, Match)