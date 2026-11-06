from http import HTTPStatus

from tennis_scoreboard.views.views import BaseView, NewMatchView
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse


class StaticPageController:

    def get_start_page(self, request: HttpRequest) -> HttpResponse:
            try:
                return HttpResponse(
                    status=HTTPStatus.OK,
                    view=BaseView()
                )
            except:
                return HttpResponse(
                    status=HTTPStatus.INTERNAL_SERVER_ERROR
                )
    
    def get_new_match_page(self, request: HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status=HTTPStatus.OK,
                view=NewMatchView()
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def get_favicon_ico(self, request: HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status=HTTPStatus.OK
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
