from tennis_scoreboard.schemas.schemas import PlayerSchema
from tennis_scoreboard.repositories.abstract import PlayerRepository


class PlayerService:

    def __init__(self, repository: PlayerRepository) -> None:
        self._repo = repository

    def get_by_id(self, id: int) -> PlayerSchema:
        player = self._repo.get_by_id(id)
        return PlayerSchema.from_sqlalchemy_model(player)

    def get_by_name(self, name: str) -> PlayerSchema:
        player = self._repo.get_by_name(name)
        return PlayerSchema.from_sqlalchemy_model(player)

    def create_player(self, name: str) -> PlayerSchema:
        player = self._repo.add(name)
        return PlayerSchema.from_sqlalchemy_model(player)