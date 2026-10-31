from typing import Any
from dataclasses import dataclass, asdict, field

from tennis_scoreboard.schemas.match_schema import MatchSchema


@dataclass
class BaseView:

    title: str = 'Tennis Scoreboard'
    template: str = 'index.html'

    def context(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class NewMatchView(BaseView):

    title: str = 'Create new match'
    template: str = 'new_match.html'

@dataclass
class MatchListView(BaseView):

    title: str = 'Matches'
    template: str = 'match_list.html'
    matches: list[MatchSchema] = field(default_factory=list)

@dataclass
class MatchScoreView(BaseView):

    title: str = 'Match score'
    template: str = 'match_score.html'
    match_schema: MatchSchema | None = field(default=None)

@dataclass
class NotFoundView(BaseView):

    title: str = 'Not Found'
    template: str = '404.html'