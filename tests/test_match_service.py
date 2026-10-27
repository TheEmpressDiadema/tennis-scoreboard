import pytest

from uuid import UUID

from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.errors.db_errors import MatchNotFoundError, PlayerNotFoundError


class TestMatchService:

    def test_create_match_with_unknown_players(self, match_service: MatchService) -> None:
        match_schema = match_service.create_match('Victor', 'Egor')
        assert match_schema.id is not None

    def test_create_match_with_one_known_players(self, match_service: MatchService, fill_players) -> None:
            match_schema = match_service.create_match('Victor', 'Misha')
            assert match_schema.id is not None

    def test_create_match_with_known_players(self, match_service: MatchService, fill_players) -> None:
        match_schema = match_service.create_match('Victor', 'Egor')
        assert match_schema.id is not None

    def test_update_match(self, match_service: MatchService, fill_matches) -> None:
        match_schema = match_service.update_match(
            UUID('00000000-0000-0000-0000-0000-00000001'),
            Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
        )
        assert match_schema.score == Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))

    def test_update_end_match(self, match_service: MatchService, fill_matches) -> None:
        match_schema = match_service.update_match(
            UUID('00000000-0000-0000-0000-0000-00000001'),
            Score(PlayerScore('0', 2, 0), PlayerScore('0', 1, 0))
        )
        assert match_schema.winner_id is not None

    def test_update_unexisting_match(self, match_service: MatchService) -> None:
        with pytest.raises(MatchNotFoundError):
            match_schema = match_service.update_match(
                UUID('00000000-0000-0000-0000-0000-00000001'),
                Score(PlayerScore('15', 0, 0), PlayerScore('0', 0, 0))
            )

    def test_get_match_by_uuid(self, match_service: MatchService, fill_matches) -> None:
        match_schema = match_service.get_match_by_uuid(UUID('00000000-0000-0000-0000-0000-00000001'))
        assert match_schema.id is not None

    def test_get_unexisting_match_by_uuid(self, match_service: MatchService) -> None:
        with pytest.raises(MatchNotFoundError):
            match_schema = match_service.get_match_by_uuid(UUID('00000000-0000-0000-0000-0000-00000001'))

    def test_get_matches(self, match_service: MatchService, fill_matches) -> None:
        match_schemas = match_service.get_matches()
        assert len(match_schemas) == 3

    def test_get_two_matches_by_page(self, match_service: MatchService, fill_matches) -> None:
        match_schemas = match_service.get_matches(count=2)
        assert len(match_schemas) == 2

    def test_get_second_page_matches(self, match_service: MatchService, fill_matches) -> None:
        match_schemas = match_service.get_matches(page=2, count=2)
        assert len(match_schemas) == 1

    def test_get_ended_player_matches(self, match_service: MatchService, fill_matches) -> None:
        match_schemas = match_service.get_player_ended_matches('Egor')
        assert len(match_schemas) == 2

    def test_get_ended_unknown_player_matches(self, match_service: MatchService) -> None:
        with pytest.raises(PlayerNotFoundError):
            match_schemas = match_service.get_player_ended_matches('Egor')