import pytest

from uuid import UUID

from tennis_scoreboard.models.models import Player
from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.repositories.unit_of_work import UnitOfWork
from tennis_scoreboard.errors.db_errors import (
    PlayerExistsError, 
    PlayerNotFoundError, 
    MatchNotFoundError
)


class TestUnitOfWork:

    def test_add_player(self, uow: UnitOfWork) -> None:
        with uow.start() as session:
            player = session.player_repository.add('Victor')
            assert player.id is not None

    def test_add_existing_player(self, uow: UnitOfWork, fill_players) -> None:
        with pytest.raises(PlayerExistsError):
            with uow.start() as session:
                player = session.player_repository.add('Victor')

    def test_get_player_by_id(self, uow: UnitOfWork, fill_players) -> None:
        with uow.start() as session:
            player = session.player_repository.get_by_id(1)
            assert player.id is not None

    def test_get_unexisting_player_by_id(self, uow: UnitOfWork) -> None:
        with pytest.raises(PlayerNotFoundError):
            with uow.start() as session:
                player = session.player_repository.get_by_id(1)

    def test_get_player_by_name(self, uow: UnitOfWork, fill_players) -> None:
        with uow.start() as session:
            player = session.player_repository.get_by_name('Dmitriy')
            assert player.id is not None

    def test_get_unexisting_player_by_name(self, uow: UnitOfWork) -> None:
        with pytest.raises(PlayerNotFoundError):
            with uow.start() as session:
                player = session.player_repository.get_by_name('Dmitriy')

    def test_add_match(self, uow: UnitOfWork, fill_players) -> None:
        with uow.start() as session:
            match_object = session.match_repository.add(Player(id=1, name='Victor'), Player(id=2, name='Dmitriy'))
            assert match_object.id != None

    def test_update_match(self, uow: UnitOfWork, fill_matches) -> None:
        with uow.start() as session:
            score = Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
            match_object = session.match_repository.update(
                UUID('00000000-0000-0000-0000-0000-00000001'),
                Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
            )
            assert match_object.score == score

    def test_update_unexisting_match(self, uow: UnitOfWork) -> None:
        with pytest.raises(MatchNotFoundError):
            with uow.start() as session:
                score = Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
                match_object = session.match_repository.update(
                    UUID('00000000-0000-0000-0000-0000-00000001'),
                    Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
                )

    def test_get_all_matches(self, uow: UnitOfWork, fill_matches) -> None:
        with uow.start() as session:
            matches = session.match_repository.get_all()
            assert len(matches) == 3

    def test_get_player_ended_matches(self, uow: UnitOfWork, fill_matches) -> None:
        with uow.start() as session:
            matches = session.match_repository.get_ended_player_matches(1)
            assert len(matches) == 1

    def test_get_unexisting_player_matches(self, uow: UnitOfWork, fill_matches) -> None:
        with uow.start() as session:
            matches = session.match_repository.get_ended_player_matches(1)
            assert len(matches) == 1

    def get_match_by_uuid(self, uow: UnitOfWork, fill_matches) -> None:
        with uow.start() as session:
            match_object = session.match_repository.get_by_uuid(UUID('00000000-0000-0000-0000-0000-00000001'))
            assert match_object.id == 1

    def test_get_unexisting_match_by_uuid(self, uow: UnitOfWork) -> None:
        with pytest.raises(MatchNotFoundError):
            with uow.start() as session:
                match_object = session.match_repository.get_by_uuid(UUID('00000000-0000-0000-0000-0000-00000001'))