from jinja2 import Environment, FileSystemLoader

from tennis_scoreboard.views.views import BaseView


class Renderer:

    def __init__(self, tempalates_path: str = 'frontend/templates/'):
        self._env = Environment(loader=FileSystemLoader(tempalates_path))

    def render(self, view: BaseView) -> bytes:
        return self._env.get_template(view.template, **view.context()).render().encode()