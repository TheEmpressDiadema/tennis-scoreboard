from uuid import uuid4, UUID

from sqlalchemy import select, or_

from tennis_scoreboard.models.models import Match, Player
from tennis_scoreboard.schemas.score import Score
from tennis_scoreboard.repositories.abstract import BaseRepository, MatchRepository
from tennis_scoreboard.errors.db_errors import MatchNotFoundError


class MatchSqlRepository(BaseRepository, MatchRepository):

    def get_all(self) -> list[Match]:
        matches = self._session.query(Match).all()
        return [obj for obj in matches]

    def get_by_uuid(self, uuid: UUID) -> Match:
        stmt = (
            select(Match).
            where(Match.uuid==uuid)
        )
        match_object = self._session.execute(stmt).scalars().one_or_none()

        if match_object is None:
            raise MatchNotFoundError

        return match_object
            

    def get_ended_player_matches(self, player_id: int) -> list[Match]:
            stmt = (
                select(Match).
                where(
                    or_(
                            Match.first_player_id==player_id, 
                            Match.second_player_id==player_id
                        ),
                    Match.winner_id.is_not(None)
                )
            )
            matches = self._session.execute(stmt).scalars()
            return [obj for obj in matches]

    def add(self, actor: Player, opponent: Player) -> Match:
        score = Score()

        match_object = Match(
            uuid=uuid4(), 
            first_player_id=actor.id, 
            second_player_id=opponent.id, 
            score=score)
        self._session.add(match_object)
        self._session.flush()
        return match_object
            

    def update(self, uuid: UUID, score: Score) -> Match:
        stmt = (
            select(Match).
            where(Match.uuid==uuid)
        )
        match_object = self._session.execute(stmt).scalars().first()
        
        if match_object is None:
            raise MatchNotFoundError

        match_object.score = score
        self._session.flush()
        return match_object