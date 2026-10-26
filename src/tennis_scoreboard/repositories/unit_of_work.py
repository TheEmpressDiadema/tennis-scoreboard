from typing import Self
from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session

from tennis_scoreboard.repositories.abstract import PlayerRepository, MatchRepository
from tennis_scoreboard.repositories.player_repository import PlayerSqlRepository
from tennis_scoreboard.repositories.match_repository import MatchSqlRepository


class UnitOfWork:

    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory
        self._session: Session

    @contextmanager
    def start(self) -> Iterator[Self]:

        self._session = self._session_factory()

        try:
            yield self
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise
        finally:
            self._session.close()

    @property
    def player_repository(self) -> PlayerRepository:
        return PlayerSqlRepository(self._session)

    @property
    def match_repository(self) -> MatchRepository:
        return MatchSqlRepository(self._session)