from tennis_scoreboard.schemas.schemas import MatchSchema
from tennis_scoreboard.repositories.abstract import MatchRepository


class MatchService:

    def __init__(self, match_repo: MatchRepository) -> None:
        self._repo = match_repo