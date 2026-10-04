from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

from tennis_scoreboard.core.db_config import DBConfig
from tennis_scoreboard.repositories.match_repository import MatchSqlRepository
from tennis_scoreboard.repositories.player_repository import PlayerSqlRepository

def get_engine() -> Engine:
    return create_engine(
            DBConfig.get_database_url('test_db_config.toml', 'server_security.toml')
        )

def get_session_factory() -> sessionmaker:
    engine = get_engine()
    session_maker = sessionmaker(engine, expire_on_commit=False)
    return session_maker

def get_player_repo():
    return PlayerSqlRepository(get_session_factory())

def get_match_repo():
    return MatchSqlRepository(get_session_factory())