from dataclasses import asdict
from typing import Any

from tennis_scoreboard.schemas.score import Score


class ScoreService:

    POSSIBLE_POINTS = ['0', '15', '30', '40']
    TIEBREAK_MAX_POINTS = 7
    SETS_TO_WIN = 2
    GAMES_TO_WIN = 6

    def _get_next_point_state(self, winner_pts: str, loser_pts: str) -> tuple[str, str]:
        if winner_pts == 'AD':
            return ('0', '0')
        if winner_pts == '40':
            if loser_pts == 'AD':
                return ('40', '40')
            if loser_pts == '40':
                return ('AD', '40')
            return ('0', '0')

        winner_idx = self.POSSIBLE_POINTS.index(winner_pts)
        return (self.POSSIBLE_POINTS[winner_idx + 1], loser_pts)

    def _is_set_won(self, winner_games: int, loser_games: int) -> bool:
        
        if winner_games == self.GAMES_TO_WIN + 1:
            return True
        
        return (
            winner_games == self.GAMES_TO_WIN
            and winner_games - loser_games >= 2
        )

    def _finish_game(
        self,
        score_dict: dict[str, Any],
        winner_score: dict[str, Any],
        loser_score: dict[str, Any],
    ) -> None:
        winner_score['games'] += 1
        winner_score['points'] = '0'
        loser_score['points'] = '0'

        if self._is_set_won(winner_score['games'], loser_score['games']):
            winner_score['sets'] += 1
            score_dict['tiebreak_flag'] = False

            if winner_score['sets'] < self.SETS_TO_WIN:
                winner_score['games'] = 0
                loser_score['games'] = 0
        else:
            
            score_dict['tiebreak_flag'] = (
                winner_score['games'] == self.GAMES_TO_WIN
                and loser_score['games'] == self.GAMES_TO_WIN
            )

    def is_match_over(self, score: Score) -> bool:
        return (
            score.first_player_score.sets >= self.SETS_TO_WIN
            or score.second_player_score.sets >= self.SETS_TO_WIN
        )

    def award_point(self, score: Score, score_to_change: str) -> Score:

        if self.is_match_over(score):
            raise ValueError

        score_dict = asdict(score)

        winner_score = score_dict[score_to_change]

        if score_to_change == 'first_player_score':
            loser_score = score_dict['second_player_score']
        else:
            loser_score = score_dict['first_player_score']

        game_ended = False

        if not score_dict['tiebreak_flag']:
            winner_score['points'], loser_score['points'] = self._get_next_point_state(
                winner_score['points'], loser_score['points']
            )
            
            game_ended = winner_score['points'] == '0'
        else:
            winner_score['points'] = str(int(winner_score['points']) + 1)
            game_ended = int(winner_score['points']) == self.TIEBREAK_MAX_POINTS

        if game_ended:
            self._finish_game(score_dict, winner_score, loser_score)

        return Score.from_dict(score_dict)