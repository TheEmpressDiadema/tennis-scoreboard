from uuid import uuid4, UUID
from typing import Any

from sqlalchemy import update, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from tennis_scoreboard.models.models import Match, Player
from tennis_scoreboard.schemas.value_objects import SetScore, Score
from tennis_scoreboard.repositories.abstract import MatchRepository
from tennis_scoreboard.errors.db_errors import MatchNotFoundError, PlayerNotFoundError


class MatchSqlRepository(MatchRepository):

    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def get_all(self) -> list[Match]:
        with self._session_factory() as session:
            try:
                matches = session.query(Match).all()
            except SQLAlchemyError:
                raise

        return matches

    def get_by_uuid(self, uuid: UUID) -> Match:
        with self._session_factory() as session:
            try:
                stmt = (
                    select(Match).
                    where(Match.uuid==uuid)
                )
                match = session.execute(stmt).scalars().one_or_none()
            except SQLAlchemyError:
                raise

            if match is None:
                raise MatchNotFoundError

        return match

    def add(self, actor: Player, opponent: Player) -> Match:
        with self._session_factory() as session:
            try:
                score = Score(
                    actor.name,
                    opponent.name
                )
                match_object = Match(
                    uuid=uuid4(), 
                    first_player_id=actor.id, 
                    second_player_id=opponent.id, 
                    score=score)
                session.add(match_object)
                session.commit()
            except IntegrityError:
                session.rollback()
                raise PlayerNotFoundError
            except SQLAlchemyError:
                    session.rollback()
                    raise

        return match_object

    def update(self, uuid: UUID, score: Score) -> Match:
        with self._session_factory() as session:
            try:
                stmt = (
                    update(Match).
                    where(Match.uuid==uuid).
                    values(score=score).
                    returning(Match)
                )
                match_object = session.execute(stmt).scalars().first()
                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise

        if match_object is None:
            raise MatchNotFoundError

        return match_object
