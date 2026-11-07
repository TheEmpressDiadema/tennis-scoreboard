from http import HTTPStatus

from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse

class StaticController:

    def get_empty_favicon(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(
            status=HTTPStatus.NO_CONTENT
        )

    def get_css(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(
            status=HTTPStatus.OK,
            headers=[('Content-type', 'text/css')]
        )
