import os
import logging
from typing import Any, Callable
from waitress import serve
from tennis_scoreboard.views.loader import TemplateLoader

static_path = os.path.join(os.getcwd(), 'frontend', 'static')
templates_path = os.path.join(os.getcwd(), 'frontend', 'templates')
template_loader = TemplateLoader()
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

ROUTES = {
    '/': 'index.html',
    '/match-score' : 'match_score.html',
    '/new-match': 'new_match.html',
    '/matches': 'match_list.html'
}

def serve_static(path: str, start_response: Callable) -> list[bytes]:
    relative_path = path.removeprefix('/static/')
    file_path = os.path.realpath(os.path.join(static_path, relative_path))

    if not os.path.isfile(file_path) or not os.path.exists(file_path):
        start_response('404 Not Found', [('Content-type', 'text/plain')])
        return [b'Not found']

    content_type = 'text/plain'
    
    if file_path.endswith('.css'):
        content_type = 'text/css'
    headers = [
        ('Content-type', content_type)
    ]
    start_response('200 OK', headers)
    with open(file_path, 'rb') as f:
        return [f.read()]

def wsgiapp(environ: dict[str, str], start_response: Callable) -> list[bytes]:
    path = environ.get('PATH_INFO', '/')
    headers = [('Content-type', 'text/html; charset=utf-8')]

    if path.startswith('/static'):
        return serve_static(path, start_response)

    template_name = ROUTES.get(path)
    if template_name is not None:
        status = '200 OK'
    else:
        status = '404 Not Found'
        template_name = '404.html'

    template = template_loader.load_template(template_name)
    start_response(status, headers)
    return [template.render().encode('utf-8')]

def main() -> None:
    serve(wsgiapp, listen='127.0.0.1:8080')