import pytest

from uuid import UUID
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Connection, create_engine, Engine

from tennis_scoreboard.core.db_config import DBConfig
from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.repositories.unit_of_work import UnitOfWork
from tennis_scoreboard.models.models import BaseModel, Player, Match

@pytest.fixture(scope='session')
def engine():
    engine = create_engine(DBConfig.get_database_url('test_db_config.toml', 'server_security.toml'))

    BaseModel.metadata.create_all(engine)

    yield engine
    
    BaseModel.metadata.drop_all(engine)

@pytest.fixture
def connection(engine: Engine):
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()

@pytest.fixture
def db_session(connection: Connection):
    session = Session(bind=connection, join_transaction_mode='create_savepoint')

    yield session

    session.rollback()
    session.close()

@pytest.fixture
def fill_matches(db_session: Session, fill_players) -> list[Match]:
    matches = [
        Match(
            id=1,
            uuid=UUID('00000000-0000-0000-0000-0000-00000001'),
            first_player_id=1,
            second_player_id=2,
            winner_id=None,
            score=Score()
        ),
        Match(
            id=2,
            uuid=UUID('00000000-0000-0000-0000-0000-00000002'),
            first_player_id=2,
            second_player_id=3,
            winner_id=2,
            score=Score(PlayerScore('0', 2, 0), PlayerScore('0', 1, 0))
        ),
        Match(
            id=3,
            uuid=UUID('00000000-0000-0000-0000-0000-00000003'),
            first_player_id=1,
            second_player_id=3,
            winner_id=1,
            score=Score(PlayerScore('0', 2, 0), PlayerScore('0', 1, 0))
        )
    ]
    db_session.add_all(matches)
    db_session.commit()
    return matches

@pytest.fixture
def fill_players(db_session: Session) -> list[Player]:

    players = [
        Player(id=1, name='Victor'),
        Player(id=2, name='Dmitriy'),
        Player(id=3, name='Egor')
    ]
    db_session.add_all(players)
    db_session.commit()
    return players

@pytest.fixture
def uow(connection: Connection) -> UnitOfWork:
    return UnitOfWork(sessionmaker(bind=connection, join_transaction_mode='create_savepoint'))

@pytest.fixture
def match_service(uow: UnitOfWork) -> MatchService:
    return MatchService(uow)