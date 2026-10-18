import pytest
from contextlib import nullcontext

from tennis_scoreboard.schemas.score import Score, PlayerScore
from tennis_scoreboard.services.score_service import ScoreService


class TestScoreService:

    _score_service = ScoreService()

    @pytest.mark.parametrize(
        'score, score_to_change, expected, raises',
        [
            (
                Score(),
                'first_player_score',
                Score(PlayerScore('15')),
                nullcontext()
            ),
            (
                Score(PlayerScore('40'), PlayerScore()), 
                'second_player_score',
                Score(PlayerScore('40'), PlayerScore('15')),
                nullcontext()
            ),
            (
                Score(PlayerScore('40'), PlayerScore('40')),
                'second_player_score',
                Score(PlayerScore('40'), PlayerScore('AD')),
                nullcontext()
            ),
            (
                Score(PlayerScore('40'), PlayerScore('AD')),
                'first_player_score',
                Score(PlayerScore('40'), PlayerScore('40')),
                nullcontext()
            ),
            (
                Score(PlayerScore('40'), PlayerScore()),
                'first_player_score',
                Score(PlayerScore('0', 0, 1)),
                nullcontext()
            ),
            (
                Score(PlayerScore('40'), PlayerScore('AD')),
                'second_player_score',
                Score(PlayerScore('0', 0, 0), PlayerScore('0', 0, 1)),
                nullcontext()
            ),
            (
                Score(PlayerScore('40', 0, 5), PlayerScore()),
                'first_player_score',
                Score(PlayerScore('0', 1, 0), PlayerScore()),
                nullcontext()
            ),
            (
                Score(PlayerScore('40', 0, 5), PlayerScore('0', 0, 0)),
                'first_player_score',
                Score(PlayerScore('0', 1, 0), PlayerScore('0', 0, 0)),
                nullcontext()
            ),
            (
                Score(PlayerScore('0', 0, 6), PlayerScore('0', 0, 6), tiebreak_flag=True),
                'first_player_score',
                Score(PlayerScore('1', 0, 6), PlayerScore('0', 0, 6), tiebreak_flag=True),
                nullcontext()
            ),
            (
                Score(PlayerScore('6', 0, 6), PlayerScore('6', 0, 6), tiebreak_flag=True),
                'first_player_score',
                Score(PlayerScore('0', 1, 0), PlayerScore('0', 0, 0), tiebreak_flag=False),
                nullcontext()
            ),
            (
                Score(PlayerScore('0', 2, 0), PlayerScore('0', 1, 0)),
                'first_player_score',
                None,
                pytest.raises(ValueError)
            )
        ]
    )
    def test_award_point(self, score: Score, score_to_change: str, expected: Score, raises: nullcontext) -> None:
        with raises:
            result = self._score_service.award_point(score, score_to_change)
            assert result == expected