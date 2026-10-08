import pytest
from contextlib import nullcontext

from tests.utils import get_match_repo, get_player_repo

from tennis_scoreboard.schemas.match_schema import MatchSchema
from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.schemas.player_schema import PlayerSchema
from tennis_scoreboard.services.match_service import MatchService


@pytest.mark.usefixtures("prepare_database")
class TestMatchService:

    _service = MatchService(
        get_match_repo(),
        get_player_repo()
    )

    @pytest.mark.parametrize(
        "expected, raises",
        [
            (MatchSchema(), nullcontext())
        ]
    )
    def test_create_match(self, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            assert 1 == 1

    @pytest.mark.parametrize(
        "expected, raises",
        [
            (MatchSchema(), nullcontext())
        ]
    )
    def test_update_match(self, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            assert 1 == 1

    @pytest.mark.parametrize(
        "expected, raises",
        [
            (MatchSchema(), nullcontext())
        ]
    )
    def test_get_player_ended_matches(self, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            assert 1 == 1

    @pytest.mark.parametrize(
        "expected, raises",
        [
            (MatchSchema(), nullcontext())
        ]
    )
    def test_get_match_by_uuid(self, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            assert 1 == 1