import pytest

from sqlalchemy.orm import Session

from tennis_scoreboard.models.models import Player
from tennis_scoreboard.repositories.player_repository import PlayerSqlRepository
from tennis_scoreboard.errors.db_errors import PlayerExistsError, PlayerNotFoundError

class TestPlayerRepository:

    def test_add_player(self, db_session: Session) -> None:
        repo = PlayerSqlRepository(db_session)
        repo.add('Victor')
        db_session.commit()

        count = db_session.query(Player).count()
        assert count == 1

    def test_add_existing_player(self, db_session: Session, fill_players) -> None:
        repo = PlayerSqlRepository(db_session)
        with pytest.raises(PlayerExistsError):
            result = repo.add('Victor')
            db_session.commit()

    def test_get_player_by_id(self, db_session: Session, fill_players) -> None:
        repo = PlayerSqlRepository(db_session)
        player = repo.get_by_id(1)
        assert player.id is not None

    def test_get_unexisting_player_by_id(self, db_session: Session) -> None:
        repo = PlayerSqlRepository(db_session)
        with pytest.raises(PlayerNotFoundError):
            player = repo.get_by_id(1)

    def test_get_player_by_name(self, db_session: Session, fill_players) -> None:
        repo = PlayerSqlRepository(db_session)
        player = repo.get_by_name('Victor')
        assert player.id is not None
    
    def test_get_unexisting_player_by_name(self, db_session: Session) -> None:
        repo = PlayerSqlRepository(db_session)
        with pytest.raises(PlayerNotFoundError):
            player = repo.get_by_id(1)