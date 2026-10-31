from http import HTTPStatus

from tennis_scoreboard.errors.db_errors import MatchNotFoundError
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.services.score_service import ScoreService
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse
from tennis_scoreboard.views.views import (
    NotFoundView, 
    NewMatchView, 
    MatchListView, 
    MatchScoreView
)


class MatchController:

    def __init__(self, match_service: MatchService, score_service: ScoreService):
        self._match_service = match_service
        self._score_service = score_service

    def create_match(self, request: HttpRequest) -> HttpResponse:
        try:
            first_player_name = request.body['first_player_name']
            second_player_name = request.body['second_player_name']
            schema = self._match_service.create_match(first_player_name, second_player_name)
            return HttpResponse(
                status=HTTPStatus.CREATED,
                view=MatchScoreView(match_schema=schema)
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def get_matches(self, request: HttpRequest) -> HttpResponse:
        try:
            schemas = self._match_service.get_matches()
            return HttpResponse(
                
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def get_match(self, request: HttpRequest) -> HttpResponse:
        try:
            uuid = request.params['uuid']
            schema = self._match_service.get_match_by_uuid(uuid)
            return HttpResponse(
                status=HTTPStatus.OK
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def update_match(self, request: HttpRequest) -> HttpResponse:
        try:
            uuid = request.params['uuid']
            score = self._match_service.get_match_by_uuid(uuid).score
            score_to_change = request.body['score_to_change']
            new_score = self._score_service.award_point(score, score_to_change)
            schema = self._match_service.update_match(uuid, new_score)
            return HttpResponse(
                status=HTTPStatus.OK
            )
        except MatchNotFoundError:
            return HttpResponse(
                status=HTTPStatus.NOT_FOUND
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def filter_matches(self, request: HttpRequest) -> HttpResponse:
        try:
            player_name = request.body['player_name']
            schemas = self._match_service.get_player_ended_matches(player_name)
            return HttpResponse(
                status=HTTPStatus.OK
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )