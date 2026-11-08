from http import HTTPStatus

from tennis_scoreboard.views.views import BaseView, NewMatchView
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse


class StaticHtmlController:

    def get_main_page(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(
            status=HTTPStatus.OK,
            view=BaseView()
        )
    
    def get_new_match_page(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(
            status=HTTPStatus.OK,
            view=NewMatchView()
        )
