from uuid import uuid4, UUID
from typing import Any

from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from tennis_scoreboard.models.models import Match, Player
from tennis_scoreboard.models.value_objects import SetScore, Score
from tennis_scoreboard.repositories.abstract import MatchRepository
from tennis_scoreboard.errors.db_errors import MatchNotFoundError, PlayerNotFoundError


class MatchSqlRepository(MatchRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Match]:

        try:
            matches = self._session.query(Match).all()
        except SQLAlchemyError:
            raise

        return matches

    def get_by_uuid(self, uuid: UUID) -> Match:

        try:
            match = self._session.get(Match, uuid)
        except SQLAlchemyError:
            raise

        if match is None:
            raise MatchNotFoundError

        return match

    def add(self, actor: Player, opponent: Player) -> Match:

        try:
            score = Score(
                first_player_name=actor.name,
                second_player_name=actor.name
            )
            match_object = Match(
                uid=uuid4(), 
                first_player_id=actor.id, 
                second_player_id=opponent.id, 
                score=score.as_dict())
            self._session.add(match_object)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise
        except IntegrityError:
            self._session.rollback()
            raise PlayerNotFoundError

        return match_object

    def update(self, uuid: UUID, score: Score) -> Match:

        try:
            stmt = (
                update(Match).
                where(Match.uuid==uuid).
                values(score=score.as_dict()).
                returning(Match)
            )
            match_object = self._session.execute(stmt).scalars().first()
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise

        if match_object is None:
            raise MatchNotFoundError

        return match_object
