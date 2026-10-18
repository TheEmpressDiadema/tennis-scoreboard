import os
from abc import abstractmethod
from typing import Protocol
from waitress import serve
from jinja2 import Environment, FileSystemLoader
from tennis_scoreboard.schemas.score import Score
from dataclasses import asdict

templates_path = os.path.join(os.getcwd(), 'src', 'tennis_scoreboard', 'view', 'templates')
env = Environment(loader=FileSystemLoader(templates_path))

ROUTES = {
    '/': 'index.html',
    '/match-score' : 'match_score.html',
    '/new-match': 'new_match.html',
    '/matches': 'match_list.html'
}

def wsgiapp(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    headers = [('Content-type', 'text/html; charset=utf-8')]

    template_name = ROUTES.get(path)
    if template_name is not None:
        status = '200 OK'
    else:
        status = '404 Not Found'

    template = env.get_template(template_name)
    start_response(status, headers)
    return [template.render().encode('utf-8')]

def main() -> None:
    # serve(wsgiapp, listen='*:8080')
    points = ['0', '15', '30', '40', 'AD']