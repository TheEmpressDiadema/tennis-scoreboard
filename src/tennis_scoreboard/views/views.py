from dataclasses import dataclass
from tennis_scoreboard.views.base import BaseView

@dataclass
class StartNewMatchView(BaseView):

    title = 'Create new match'
    template_name = 'new_match.html'


@dataclass
class MatchView(BaseView):

    title = 'Match page'
    template_name = 'match_score.html'