import pytest

from uuid import UUID
from sqlalchemy.orm import Session

from tennis_scoreboard.models.models import Match, Player
from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.errors.db_errors import PlayerNotFoundError, MatchNotFoundError
from tennis_scoreboard.repositories.match_repository import MatchSqlRepository


class TestMatchRepository:

    def test_add_match(self, db_session: Session, fill_players) -> None:
        repo = MatchSqlRepository(db_session)
        match_object = repo.add(Player(id=1, name='Victor'), Player(id=2, name='Dmitriy'))
        db_session.commit()

        count = db_session.query(Match).count()
        assert count == 1

    def test_update_match(self, db_session: Session, fill_matches) -> None:
        repo = MatchSqlRepository(db_session)
        score = Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
        match_object = repo.update(
            UUID('00000000-0000-0000-0000-0000-00000001'), 
            score
        )
        db_session.commit()
        assert match_object.score == score

    def test_update_unexisting_match(self, db_session: Session, fill_matches) -> None:
        repo = MatchSqlRepository(db_session)
        score = Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
        with pytest.raises(MatchNotFoundError):
            match_object = repo.update(
                UUID('00000000-0000-0000-0000-0000-00000004'), 
                score
            )

    def test_get_all_matches(self, db_session: Session, fill_matches) -> None:
        repo = MatchSqlRepository(db_session)
        matches = repo.get_all()
        assert len(matches) == 3

    def test_get_player_ended_matches(self, db_session: Session, fill_matches) -> None:
        repo = MatchSqlRepository(db_session)
        matches = repo.get_ended_player_matches(1)
        assert len(matches) == 1

    def test_get_unexisting_player_matches(self, db_session: Session, fill_matches) -> None:
        repo = MatchSqlRepository(db_session)
        matches = repo.get_ended_player_matches(4)
        assert len(matches) == 0

    def get_match_by_uuid(self, db_session: Session, fill_matches) -> None:
        repo = MatchSqlRepository(db_session)
        match_object = repo.get_by_uuid(UUID('00000000-0000-0000-0000-0000-00000001'))
        assert match_object.id is not None

    def test_get_unexisting_match_by_uuid(self, db_session: Session) -> None:
        repo = MatchSqlRepository(db_session)
        with pytest.raises(MatchNotFoundError):
            match_object = repo.get_by_uuid(UUID('00000000-0000-0000-0000-0000-00000001'))