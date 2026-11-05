from http import HTTPStatus

from tennis_scoreboard.errors.score_errors import MatchEnded
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.services.score_service import ScoreService
from tennis_scoreboard.errors.db_errors import MatchNotFoundError
from tennis_scoreboard.controllers.structures import HttpRequest, HttpResponse
from tennis_scoreboard.views.views import (
    MatchScoreView,
    MatchListView,
    NotFoundView,
    BaseView,
    NewMatchView
)

class MatchController:

    def __init__(self, match_service: MatchService, score_service: ScoreService):
        self._match_service = match_service
        self._score_service = score_service

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

    def get_create_match_page(self, request: HttpRequest) -> HttpResponse:
        try:
            return HttpResponse(
                status=HTTPStatus.OK,
                view=NewMatchView()
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    def create_match(self, request: HttpRequest) -> HttpResponse:
        try:
            first_player_name = request.body['first_player_name']
            second_player_name = request.body['second_player_name']
            schema = self._match_service.create_match(first_player_name, second_player_name)
            location = '/match-score?uuid=' + schema.uuid
            return HttpResponse.redirect(location)
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def update_match(self, request: HttpRequest) -> HttpResponse:
        try:
            uuid = request.params['uuid']
            score_to_change = request.body['score_to_change']
            schema = self._match_service.get_match_by_uuid(uuid)
            result_score = self._score_service.award_point(schema.score, score_to_change)

            updated_match = self._match_service.update_match(uuid, result_score)
            return HttpResponse(
                status=HTTPStatus.OK,
                view=MatchScoreView(match_schema=updated_match)
            )
        except MatchNotFoundError:
            return HttpResponse(
                status=HTTPStatus.NOT_FOUND,
                view=NotFoundView()
            )
        except MatchEnded:
            return HttpResponse(
                status=HTTPStatus.IM_A_TEAPOT,
                view=MatchScoreView(match_schema=schema)
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
                status=HTTPStatus.OK,
                view=MatchScoreView(match_schema=schema)
            )
        except MatchNotFoundError:
            return HttpResponse(
                status=HTTPStatus.NOT_FOUND,
                view=NotFoundView()
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def get_matches(self, request: HttpRequest) -> HttpResponse:
        try:
            player_name = request.body.get('filter_by_player_name')
            page = request.params.get('page_number')

            if page is None:
                page = 1
            else:
                page = int(page)

            if player_name is None:
                schemas = self._match_service.get_ended_matches(page=page)
            else:
                schemas = self._match_service.get_player_ended_matches(player_name, page=page)
            
            return HttpResponse(
                status=HTTPStatus.OK,
                view=MatchListView(matches=schemas)
            )
        except:
            return HttpResponse(
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )