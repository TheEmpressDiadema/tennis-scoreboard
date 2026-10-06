import pytest

from uuid import UUID
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import insert

from tests.utils import get_engine
from tennis_scoreboard.schemas.schemas import Score
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
            score=Score('Victor', 'Dmitriy')
            ),
        Match(
            uuid=UUID(hex='00000000-0000-0000-0000-000000000002'),
            first_player_id=2,
            second_player_id=3,
            score=Score('Dmitriy', 'Egor')
        )
    ]
    with session_factory() as session:
        for match in matches:
            stmt = insert(Match).values(
                {
                    'uuid' : match.uuid,
                    'first_player_id' : match.first_player_id,
                    'second_player_id' : match.second_player_id,
                    'score' : match.score
                }
            )
            session.execute(stmt)
        session.commit()

def _fill_table(engine: Engine, model: type[BaseModel]) -> None:
    session_maker = sessionmaker(engine)

    if model == Player:
        _fill_player(session_maker)
    if model == Match:
        _fill_matches(session_maker)

@pytest.fixture(scope='session', autouse=True)
def prepare_database() -> None:
    engine = get_engine()
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
    
    _fill_table(engine, Player)
    _fill_table(engine, Match)