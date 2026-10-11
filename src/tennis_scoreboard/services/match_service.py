from uuid import UUID

from tennis_scoreboard.errors.db_errors import PlayerNotFoundError
from tennis_scoreboard.repositories.abstract import MatchRepository, PlayerRepository
from tennis_scoreboard.schemas.match_schema import MatchSchema
from tennis_scoreboard.schemas.score import Score


class MatchService:

    def __init__(self, match_repo: MatchRepository, player_repo: PlayerRepository) -> None:
        self._match_repo = match_repo
        self._player_repo = player_repo

    def create_match(self, actor_name: str, opponent_name: str) -> MatchSchema:

        try:
            actor = self._player_repo.get_by_name(actor_name)
        except PlayerNotFoundError:
            actor = self._player_repo.add(actor_name)

        try:
            opponent = self._player_repo.get_by_name(opponent_name)
        except PlayerNotFoundError:
            opponent = self._player_repo.add(opponent_name)


        match = self._match_repo.add(
            actor,
            opponent
        )
        return MatchSchema.from_sqlalchemy_model(match)
    
    def update_match(self, uuid: UUID, score: Score) -> MatchSchema:        
        match = self._match_repo.update(
            uuid,
            score
        )
        return MatchSchema.from_sqlalchemy_model(match)

    def get_match_by_uuid(self, uuid: UUID) -> MatchSchema:
        return MatchSchema.from_sqlalchemy_model(
            self._match_repo.get_by_uuid(uuid)
        )

    def get_player_ended_matches(self, name: str) -> list[MatchSchema]:
        player = self._player_repo.get_by_name(name)
        matches = self._match_repo.get_ended_player_matches(player.id)

        schemas = [MatchSchema.from_sqlalchemy_model(match) for match in matches]
        return schemas

    def get_matches(self, page: int = 1, count: int = 5) -> list[MatchSchema]:

        matches = self._match_repo.get_all()

        lower_bound = count*(page - 1)
        upper_bound = min(page * count + 1, len(matches))

        return [MatchSchema.from_sqlalchemy_model(matches[i]) for i in range(lower_bound, upper_bound)]