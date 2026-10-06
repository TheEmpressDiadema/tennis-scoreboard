from uuid import uuid4, UUID

from sqlalchemy import select, and_, or_
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from tennis_scoreboard.models.models import Match, Player
from tennis_scoreboard.schemas.schemas import Score
from tennis_scoreboard.repositories.abstract import MatchRepository
from tennis_scoreboard.errors.db_errors import MatchNotFoundError, PlayerNotFoundError


class MatchSqlRepository(MatchRepository):

    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory

    def get_all(self) -> list[Match]:
        with self._session_factory() as session:
            try:
                matches = session.query(Match).all()
                return matches
            except SQLAlchemyError:
                raise

    def get_by_uuid(self, uuid: UUID) -> Match:
        with self._session_factory() as session:
            try:
                stmt = (
                    select(Match).
                    where(Match.uuid==uuid)
                )
                match = session.execute(stmt).scalars().one_or_none()

                if match is None:
                    raise MatchNotFoundError

                return match
            except SQLAlchemyError:
                raise

    def get_matches_by_player_id(self, player_id: int) -> list[Match]:
        with self._session_factory() as session:
            try:
                stmt = (
                    select(Match).
                    where(
                        and_(
                            or_(
                                Match.first_player_id==player_id, 
                                Match.second_player_id==player_id
                            ),
                            Match.winner_id.is_not(None)
                        )
                    )
                )
                matches = session.execute(stmt).scalars()
                return list(matches)
            except SQLAlchemyError:
                raise

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

                return match_object
            except IntegrityError:
                session.rollback()
                raise PlayerNotFoundError
            except SQLAlchemyError:
                    session.rollback()
                    raise

    def update(self, uuid: UUID, score: Score) -> Match:
        with self._session_factory() as session:
            stmt = (
                select(Match).
                where(Match.uuid==uuid)
            )
            match = session.execute(stmt).scalars().first()
            
            if match is None:
                raise MatchNotFoundError

            match.score = score

            try:
                session.commit()
                return match
            except IntegrityError:
                session.rollback()
                raise