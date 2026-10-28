from jinja2 import Environment, FileSystemLoader, Template


class TemplateLoader:

    def __init__(self, templates_dir: str = 'frontend/templates'):
        self._env = Environment(loader=FileSystemLoader(templates_dir))

    def load_template(self, template_name: str) -> Template:
        return self._env.get_template(template_name)