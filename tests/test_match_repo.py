import pytest

from contextlib import nullcontext

from tests.utils import get_match_repo
from tennis_scoreboard.models.models import Player, Match
from tennis_scoreboard.errors.db_errors import (
    PlayerNotFoundError,
    MatchNotFoundError
)


class TestMatchSqlRepository:

    _repo = get_match_repo()

    @pytest.mark.parametrize(
        "actor, opponent, expected, raises",
        [
            (Player(id=1, name='Victor'), Player(id=2, name='Dmitriy'),
             Match(id=1, first_player_id=1, second_player_id=2), nullcontext()),
        ]
    )
    def test_add(self, actor: Player, opponent: Player, expected: Match, raises: nullcontext) -> None:
        with raises:
            match = self._repo.add(actor, opponent)
            assert match.id == expected.id