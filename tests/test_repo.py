import pytest

from uuid import UUID
from contextlib import nullcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

from tennis_scoreboard.core.db_config import DBConfig
from tennis_scoreboard.repositories.match_repository import MatchSqlRepository
from tennis_scoreboard.repositories.player_repository import PlayerSqlRepository
from tennis_scoreboard.errors.db_errors import (
    PlayerExistsError, 
    PlayerNotFoundError,
    MatchNotFoundError
)
from tennis_scoreboard.models.models import (
    BaseModel,
    Player, #noqa
    Match #noqa
)

def create_session() -> Session:
    engine = create_engine(
            DBConfig.get_database_url("test_db_config.toml", "server_security.toml"),
        )
    session_factory = sessionmaker(engine)
    return session_factory()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    engine = create_engine(
        DBConfig.get_database_url("test_db_config.toml", "server_security.toml")
    )
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)

@pytest.mark.usefixtures("setup_database")
class TestPlayerSQLRepository:        

    @pytest.mark.parametrize(
        "name, expected, raises",
        [
            ("Dmitriy", Player(id=1, name="Dmitriy"), nullcontext()),
            ("Victor", Player(id=2, name="Victor"), nullcontext()),
            ("Alexey", Player(id=3, name="Alexey"), nullcontext()),
            ("Vasya", Player(id=4, name="Vasya"), nullcontext()),
            ("Victor", None, pytest.raises(PlayerExistsError)),
            ("Dmitriy", None, pytest.raises(PlayerExistsError))
        ]
    )
    def test_add(self, name: str, expected: Player, raises: nullcontext) -> None:
        repo = PlayerSqlRepository(create_session())

        with raises:
            player = repo.add(name)
            assert player.id == expected.id
            assert player.name == expected.name


    @pytest.mark.parametrize(
        "id, expected, raises",
        [
            (1, Player(id=1, name="Dmitriy"), nullcontext()),
            (2, Player(id=2, name="Victor"), nullcontext()),
            (3, Player(id=3, name="Alexey"), nullcontext()),
            (5, None, pytest.raises(PlayerNotFoundError)),
            (6, None, pytest.raises(PlayerNotFoundError))
        ]
    )
    def test_get(self, id: int, expected: Player, raises: nullcontext) -> None:
        repo = PlayerSqlRepository(create_session())

        with raises:
            player = repo.get_by_id(id)
            assert player.id == expected.id
            assert player.name == expected.name