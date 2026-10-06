import pytest

from contextlib import nullcontext

from tennis_scoreboard.errors.db_errors import (
    PlayerExistsError, 
    PlayerNotFoundError
)
from tennis_scoreboard.models.models import (
    Player
)
from tests.utils import get_player_repo


@pytest.mark.usefixtures("prepare_database")
class TestPlayerSqlRepository:

    _repo = get_player_repo()

    @pytest.mark.parametrize(
        "name, expected, raises",
        [
            ('Sergey', Player(id=4, name='Sergey'), nullcontext()),
            ('Nikolay', Player(id=5, name='Nikolay'), nullcontext()),
            ('Victor', Player(id=1, name='Victor'), pytest.raises(PlayerExistsError)),
            ('Dmitriy', Player(id=2, name='Dmitriy'), pytest.raises(PlayerExistsError))
        ]
    )
    def test_add(self, name: str, expected: Player, raises: nullcontext) -> None:
        with raises:
            player = self._repo.add(name)
            assert player.id == expected.id

    @pytest.mark.parametrize(
            "id, expected, raises",
            [
                (1, Player(id=1, name='Victor'), nullcontext()),
                (3, Player(id=3, name='Egor'), nullcontext()),
                (6, None, pytest.raises(PlayerNotFoundError))
            ]
    )
    def test_get_by_id(self, id: int, expected: Player, raises: nullcontext) -> None:
        with raises:
            player = self._repo.get_by_id(id)
            assert player.name == expected.name

    @pytest.mark.parametrize(
        "name, expected, raises",
        [
            ('Victor', Player(id=1, name='Victor'), nullcontext()),
            ('Dmitriy', Player(id=2, name='Victor'), nullcontext()),
            ('Konstantin', None, pytest.raises(PlayerNotFoundError))
        ]
    )
    def test_get_by_name(self, name: str, expected: Player, raises: nullcontext) -> None:
        with raises:
            player = self._repo.get_by_name(name)
            assert player.id == expected.id