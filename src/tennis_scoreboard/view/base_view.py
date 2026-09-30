from abc import ABC

from jinja2 import Environment
from jinja2 import BaseLoader, FileSystemLoader

class BaseView(ABC):

    def __init__(self, file_loader: BaseLoader):
        self._env = Environment(loader=file_loader)