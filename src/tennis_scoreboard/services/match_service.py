from uuid import UUID

from tennis_scoreboard.schemas.score import Score
from tennis_scoreboard.schemas.match_schema import MatchSchema
from tennis_scoreboard.errors.db_errors import PlayerNotFoundError
from tennis_scoreboard.repositories.unit_of_work import UnitOfWork


class MatchService:

    def __init__(self, unit_of_work: UnitOfWork) -> None:
        self._unit_of_work = unit_of_work

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


            match = session.match_repository.add(
                actor,
                opponent
            )
        
            return MatchSchema.from_sqlalchemy_model(match)
    
    def update_match(self, uuid: UUID, score: Score) -> MatchSchema:  
        with self._unit_of_work.start() as session:      
            match = session.match_repository.update(
                uuid,
                score
            )
            return MatchSchema.from_sqlalchemy_model(match)

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
            upper_bound = min(page * count + 1, len(matches))

            return [MatchSchema.from_sqlalchemy_model(matches[i]) for i in range(lower_bound, upper_bound)]