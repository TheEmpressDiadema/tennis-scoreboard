import pytest
from uuid import UUID
from contextlib import nullcontext

from tests.utils import get_match_repo, get_player_repo

from tennis_scoreboard.schemas.match_schema import MatchSchema
from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.schemas.player_schema import PlayerSchema
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.errors.db_errors import MatchNotFoundError


@pytest.mark.usefixtures("prepare_database")
class TestMatchService:

    _service = MatchService(
        get_match_repo(),
        get_player_repo()
    )

    @pytest.mark.parametrize(
        "actor_name, opponent_name, expected, raises",
        [
            (
            'Victor', 'Dmitriy',
            MatchSchema(
                id=4, 
                first_player=PlayerSchema('Dmitriy'), 
                second_player=PlayerSchema('Victor'),
                score=Score(),
            ),
            nullcontext()
            ),
            (
                'Koka', 'Kuka',
                MatchSchema(
                    id=5,
                    first_player=PlayerSchema('Koka'),
                    second_player=PlayerSchema('Kuka'),
                    score=Score()
                ),
                nullcontext()
            )
        ]
    )
    def test_create_match(self, actor_name: str, opponent_name: str, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            match_schema = self._service.create_match(actor_name, opponent_name)
            assert match_schema.id == expected.id

    @pytest.mark.parametrize(
        "uuid, score, expected, raises",
        [
            (
                UUID('00000000-0000-0000-0000-000000000001'), 
                Score(
                    PlayerScore('15', 0, 0),
                    PlayerScore('15', 0, 0)
                ),
                MatchSchema(
                    id=1,
                    first_player=PlayerSchema(name='Victor'),
                    second_player=PlayerSchema(name='Dmitriy'),
                    score=Score(
                        PlayerScore('15', 0, 0),
                        PlayerScore('15', 0, 0)
                    )
                ), 
                nullcontext()
            ),
            (
                UUID('00000000-0000-0000-0000-000000000008'),
                None,
                None,
                pytest.raises(MatchNotFoundError)
            )
        ]
    )
    def test_update_match(self, uuid: UUID, score: Score, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            match_schema = self._service.update_match(uuid, score)
            assert match_schema.score == expected.score

    @pytest.mark.parametrize(
        "name, expected, raises",
        [
            ('Dmitriy', 1, nullcontext()),
            ('Victor', 1, nullcontext()),
            ('Egor', 0, nullcontext())
        ]
    )
    def test_get_player_ended_matches(self, name: str, expected: int, raises: nullcontext) -> None:
        with raises:
            matches = self._service.get_player_ended_matches(name)
            assert len(matches) == expected

    @pytest.mark.parametrize(
        "uuid, expected, raises",
        [
            (
                UUID('00000000-0000-0000-0000-000000000001'),
                MatchSchema(
                    id=1,
                    uuid=UUID('00000000-0000-0000-0000-000000000001'),
                    first_player=PlayerSchema(name='Victor', id=1),
                    second_player=PlayerSchema(name='Dmitriy', id=2),
                    score=Score(
                        PlayerScore('15', 0, 0),
                        PlayerScore('15', 0, 0)
                    )
                ), 
                nullcontext()
            ),
            (
                UUID('00000000-0000-0000-0000-000000000008'),
                None,
                pytest.raises(MatchNotFoundError)
            )
        ]
    )
    def test_get_match_by_uuid(self, uuid: UUID, expected: MatchSchema, raises: nullcontext) -> None:
        with raises:
            match_schema = self._service.get_match_by_uuid(uuid)
            assert match_schema.id == expected.id