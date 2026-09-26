from waitress import serve


def wsgiapp(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)

    return [b'Hello from pure Python WSGI']

def main() -> None:
    serve(wsgiapp, listen='*:8080')
