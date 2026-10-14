from tennis_scoreboard.core.structures import HttpRequest, HttpResponse
from tennis_scoreboard.services.match_service import MatchService


class MatchController:

    def __init__(self, service: MatchService):
        self._service = service

    def create_match(self, request: HttpRequest) -> HttpResponse:
        try:
            first_player = request['first_player']
            second_player = request['second_player']

            return HttpResponse(200, 'jopa')
        except:
            return HttpResponse(400, 'gg')