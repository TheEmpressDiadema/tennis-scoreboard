from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from tennis_scoreboard.models.models import Player
from tennis_scoreboard.errors.db_errors import PlayerExistsError, PlayerNotFoundError
from tennis_scoreboard.repositories.abstract import BaseRepository, PlayerRepository


class PlayerSqlRepository(BaseRepository, PlayerRepository):

    def add(self, name: str) -> Player:
        try:
            player = Player(name=name)
            self._session.add(player)
            self._session.flush()
            return player
        except IntegrityError:
            raise PlayerExistsError

    def get_by_id(self, id: int) -> Player:
        player = self._session.get(Player, id)

        if player is None:
            raise PlayerNotFoundError

        return player
    
    def get_by_name(self, name: str) -> Player:
        stmt = (
            select(Player).
            where(Player.name==name)
        )
        player = self._session.execute(stmt).scalar_one_or_none()

        if player is None:
            raise PlayerNotFoundError

        return player