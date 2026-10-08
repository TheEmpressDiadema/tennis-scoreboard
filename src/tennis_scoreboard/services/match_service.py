from uuid import UUID
from typing import Any

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

    def update_match(self, uuid: UUID, score: dict[str, Any]) -> MatchSchema:
        target_score = Score.from_dict(score)
        match = self._match_repo.update(
            uuid,
            target_score
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