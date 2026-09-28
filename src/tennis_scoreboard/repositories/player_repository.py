from sqlalchemy.orm import Session

from tennis_scoreboard.models.models import Player
from tennis_scoreboard.errors.db_errors import PlayerExistsError
from tennis_scoreboard.repositories.abstract import PlayerRepository


class PlayerSQLRepository(PlayerRepository):

    def __init__(self, session: Session) -> None:
        self._session: Session = session

    def add(self, name: str) -> Player:
        return Player()