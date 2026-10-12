from jinja2 import Environment
from jinja2 import FileSystemLoader

class ViewEngine:

    def __init__(self, file_loader: FileSystemLoader = FileSystemLoader('frontend/')):
        self._env = Environment(loader=file_loader)

    def draw_template(self, template_path: str) -> None:
        pass