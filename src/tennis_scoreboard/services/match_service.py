from uuid import UUID
from typing import Any
from tennis_scoreboard.repositories.abstract import MatchRepository, PlayerRepository
from tennis_scoreboard.schemas.schemas import MatchSchema, PlayerSchema, Score


class MatchService:

    def __init__(self, match_repo: MatchRepository, player_repo: PlayerRepository) -> None:
        self._match_repo = match_repo
        self._player_repo = player_repo

    def create_match(self, actor: str, opponent: str) -> MatchSchema:
        match = self._match_repo.add(
            PlayerSchema(name=actor).to_sqlalchemy_model(),
            PlayerSchema(name=opponent).to_sqlalchemy_model()
        )
        return MatchSchema.from_sqlalchemy_model(match)

    def update_match(self, uuid: str, score: dict[str, Any]) -> MatchSchema:
        target_uuid = UUID(uuid)
        target_score = Score.from_dict(score)
        match = self._match_repo.update(
            target_uuid,
            target_score
        )
        return MatchSchema.from_sqlalchemy_model(match)

    def get_matches_by_player_name(self, name: str) -> list[MatchSchema]:
        player = self._player_repo.get_by_name(name)
        matches = self._match_repo.get_matches_by_player_id(player.id)

        schemas = [MatchSchema.from_sqlalchemy_model(match) for match in matches]
        return schemas