import pytest

from uuid import UUID, uuid4
from contextlib import nullcontext
from sqlalchemy.exc import IntegrityError

from tests.utils import get_match_repo
from tennis_scoreboard.models.models import Player, Match
from tennis_scoreboard.schemas.value_objects import Score, SetScore
from tennis_scoreboard.errors.db_errors import (
    PlayerNotFoundError,
    MatchNotFoundError
)

@pytest.mark.usefixtures('prepare_database')
class TestMatchSqlRepository:

    _repo = get_match_repo()

    @pytest.mark.parametrize(
        "actor, opponent, expected, raises",
        [
            (
                Player(id=1, name='Victor'), Player(id=2, name='Dmitriy'),
                Match(id=3, first_player_id=1, second_player_id=2), nullcontext()
            ),
            (
                Player(id=1, name='Victor'), Player(id=6, name='Aleksandr'),
                None, pytest.raises(PlayerNotFoundError)
            )
        ]
    )
    def test_add(self, actor: Player, opponent: Player, expected: Match, raises: nullcontext) -> None:
        with raises:
            match = self._repo.add(actor, opponent)
            assert match.id == expected.id

    @pytest.mark.parametrize(
        "uuid, expected, raises",
        [
            (
                UUID(hex='00000000-0000-0000-0000-000000000001'),
                Match(
                    id=1, 
                    first_player_id=1, 
                    second_player_id=2, 
                    score=Score('Victor', 'Dmitriy')
                ),
                nullcontext()
            ),
            (
                UUID(hex='00000000-0000-0000-0000-000000000002'),
                Match(
                    id=2, 
                    first_player_id=2, 
                    second_player_id=3, 
                    score=Score('Dmitriy', 'Egor')
                ),
                nullcontext()
            ),
            (
                uuid4(),
                None,
                pytest.raises(MatchNotFoundError)
            )
        ]
    )
    def test_get_by_uuid(self, uuid: UUID, expected: Match, raises: nullcontext) -> None:
        with raises:
            match = self._repo.get_by_uuid(uuid)
            assert match.id == expected.id

    @pytest.mark.parametrize(
        "length, raises",
        [
            (nullcontext())
        ]
    )
    def get_all(self, length: int, raises: nullcontext) -> None:
        with raises:
            matches = self._repo.get_all()
            assert length == len(matches)

    @pytest.mark.parametrize(
        "uuid, score, expected, raises",
        [
            (
                UUID(hex='00000000-0000-0000-0000-000000000001'),
                Score('Victor', 'Dmitriy', first_set=SetScore(15, 0)),
                Score('Victor', 'Dmitriy', first_set=SetScore(15, 0)),
                nullcontext()
            ),
            (
                UUID(hex='00000000-0000-0000-0000-000000000002'),
                Score('Dmitriy', 'Victor', first_set=SetScore(15, 0)),
                Score('Dmitriy', 'Victor', first_set=SetScore(15, 0)),
                nullcontext()
            ),
            (
                uuid4(),
                Score('Egor', 'Aleksandr', first_set=SetScore(0, 15)),
                None,
                pytest.raises(MatchNotFoundError)
            )
        ]
    )
    def test_update(self, uuid: UUID, score: Score, expected: Score, raises: nullcontext) -> None:
        with raises:
            match = self._repo.update(uuid, score)
            assert match.score == expected