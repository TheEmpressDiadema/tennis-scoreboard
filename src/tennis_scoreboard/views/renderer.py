import os

from jinja2 import Environment, FileSystemLoader

from tennis_scoreboard.views.views import BaseView


class Renderer:

    _STATIC_DIR = 'frontend/static'

    def __init__(self, tempalates_path: str = 'frontend/templates/'):
        self._env = Environment(loader=FileSystemLoader(tempalates_path))

    def render(self, view: BaseView | None) -> bytes:
        if view is not None:
            return self._env.get_template(name=view.template).render(**view.context()).encode()
        return b''

    def render_css(self, path: str) -> bytes:
        filename = path.removeprefix('/static/')
        file_path = os.path.join(self._STATIC_DIR, filename)

        with open(file_path, 'r', encoding='utf-8') as css:
            return css.read().encode()