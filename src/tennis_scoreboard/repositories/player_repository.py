from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from tennis_scoreboard.models.models import Player
from tennis_scoreboard.errors.db_errors import PlayerExistsError, PlayerNotFoundError
from tennis_scoreboard.repositories.abstract import PlayerRepository


class PlayerSqlRepository(PlayerRepository):

    def __init__(self, session: Session) -> None:
        self._session: Session = session

    def add(self, name: str) -> Player:

        try:

            player = Player(name=name)
            self._session.add(player)
            self._session.commit()
        
        except IntegrityError:

            self._session.rollback()
            raise PlayerExistsError
        
        except SQLAlchemyError:

            self._session.rollback()
            raise

        return player

    def get_by_id(self, id: int) -> Player:
        try:
            player = self._session.get(Player, id)
        except SQLAlchemyError:
            raise

        if player is None:
            raise PlayerNotFoundError

        return player