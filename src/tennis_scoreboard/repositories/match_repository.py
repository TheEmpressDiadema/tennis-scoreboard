from uuid import uuid4
from typing import Any
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from tennis_scoreboard.models.models import Match, Player
from tennis_scoreboard.errors.db_errors import MatchNotFoundError
from tennis_scoreboard.repositories.abstract import MatchRepository


class MatchSQLRepository(MatchRepository):

    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Match]:

        try:
            matches = self._session.query(Match).all()
        except SQLAlchemyError:
            raise

        return matches

    def get_by_id(self, id: int) -> Match:

        try:
            match = self._session.get(Match, id)
        except SQLAlchemyError:
            raise

        if match is None:
            raise MatchNotFoundError

        return match

    def add(self, actor: Player, opponent: Player) -> Match:

        try:
            match_object = Match(uid=uuid4(), first_player=actor, second_player=opponent, score={})
            self._session.add(match_object)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()

            raise 

        return match_object

    def update(self, id: int, score: dict[str, Any]) -> Match:

        try:
            stmt = (
                update(Match).
                where(Match.id==id).
                values(score=score).
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
