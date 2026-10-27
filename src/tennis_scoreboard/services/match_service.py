from uuid import UUID

from tennis_scoreboard.schemas.score import Score
from tennis_scoreboard.models.models import Match
from tennis_scoreboard.schemas.match_schema import MatchSchema
from tennis_scoreboard.errors.db_errors import PlayerNotFoundError
from tennis_scoreboard.repositories.unit_of_work import UnitOfWork


class MatchService:

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

    def _define_winner(self, match_object: Match, new_score: Score) -> int | None:
        if new_score.first_player_score.sets == 2:
            return match_object.first_player.id
        if new_score.second_player_score.sets == 2:
            return match_object.second_player.id
        return None

    def create_match(self, actor_name: str, opponent_name: str) -> MatchSchema:
        with self._unit_of_work.start() as session:
            try:
                actor = session.player_repository.get_by_name(actor_name)
            except PlayerNotFoundError:
                actor = session.player_repository.add(actor_name)

            try:
                opponent = session.player_repository.get_by_name(opponent_name)
            except PlayerNotFoundError:
                opponent = session.player_repository.add(opponent_name)


            match_object = session.match_repository.add(
                actor,
                opponent
            )
        
            return MatchSchema.from_sqlalchemy_model(match_object)

    def update_match(self, uuid: UUID, score: Score) -> MatchSchema:  
        with self._unit_of_work.start() as session:
            match_object = session.match_repository.get_by_uuid(uuid)

            winner_id = self._define_winner(match_object, score)

            match_schema = session.match_repository.update(
                uuid,
                score,
                winner_id=winner_id
            )
            return MatchSchema.from_sqlalchemy_model(match_schema)

    def get_match_by_uuid(self, uuid: UUID) -> MatchSchema:
        with self._unit_of_work.start() as session:
            return MatchSchema.from_sqlalchemy_model(
                session.match_repository.get_by_uuid(uuid)
            )

    def get_player_ended_matches(self, name: str) -> list[MatchSchema]:
        with self._unit_of_work.start() as session:
            player = session.player_repository.get_by_name(name)
            matches = session.match_repository.get_ended_player_matches(player.id)

            schemas = [MatchSchema.from_sqlalchemy_model(match) for match in matches]
            return schemas

    def get_matches(self, page: int = 1, count: int = 5) -> list[MatchSchema]:
        with self._unit_of_work.start() as session:
            matches = session.match_repository.get_all()

            lower_bound = count*(page - 1)
            upper_bound = min(page * count, len(matches))

            return [MatchSchema.from_sqlalchemy_model(matches[i]) for i in range(lower_bound, upper_bound)]