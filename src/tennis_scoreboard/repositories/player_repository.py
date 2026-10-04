from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from tennis_scoreboard.models.models import Player
from tennis_scoreboard.errors.db_errors import PlayerExistsError, PlayerNotFoundError
from tennis_scoreboard.repositories.abstract import PlayerRepository


class PlayerSqlRepository(PlayerRepository):

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def add(self, name: str) -> Player:

        with self._session_factory() as session:
            try:
                player = Player(name=name)
                session.add(player)
                session.commit()
            except IntegrityError:
                session.rollback()
                raise PlayerExistsError
            except SQLAlchemyError:
                session.rollback()
                raise

        return player

    def get_by_id(self, id: int) -> Player:
        with self._session_factory() as session:
            try:
                player = session.get(Player, id)
            except SQLAlchemyError:
                raise

        if player is None:
            raise PlayerNotFoundError

        return player