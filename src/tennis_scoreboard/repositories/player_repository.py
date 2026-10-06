from sqlalchemy import select
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

                return player
            except IntegrityError:
                session.rollback()
                raise PlayerExistsError
            except SQLAlchemyError:
                session.rollback()
                raise

    def get_by_id(self, id: int) -> Player:
        with self._session_factory() as session:
            try:
                player = session.get(Player, id)

                if player is None:
                    raise PlayerNotFoundError
        
                return player
            except SQLAlchemyError:
                raise

    def get_by_name(self, name: str) -> Player:
        with self._session_factory() as session:
            try:
                stmt = (
                    select(Player).
                    where(Player.name==name)
                )
                player = session.execute(stmt).scalar_one_or_none()

                if player is None:
                    raise PlayerNotFoundError

                return player
            except SQLAlchemyError:
                raise