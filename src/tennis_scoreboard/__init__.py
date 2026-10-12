from waitress import serve
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('src/frontend/'))

def wsgiapp(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]

    template = env.get_template('index.html')
    html = template.render()

    start_response(status, headers)

    return [html.encode('utf-8')]

def main() -> None:
    serve(wsgiapp, listen='*:8080')