from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.services.score_service import ScoreService


class MatchController:

    def __init__(self, match_service: MatchService, score_service: ScoreService):
        self._match_service = match_service
        self._score_service = score_service