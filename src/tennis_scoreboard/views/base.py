from dataclasses import dataclass

from tennis_scoreboard.views.loader import TemplateLoader


@dataclass
class BaseView:

    title = 'Tennis scoreboard'
    template_name = 'index.html'