import pytest

from http import HTTPStatus

from tennis_scoreboard.controllers.match_controller import MatchController
from tennis_scoreboard.controllers.structures import HttpResponse, HttpRequest
from tennis_scoreboard.views.views import (
    MatchListView,
    MatchScoreView,
    NewMatchView,
    NotFoundView
)


class TestMatchController:

    def test_create_match(self, match_controller: MatchController, fill_players) -> None:
        response = match_controller.create_match(
            HttpRequest(
                method='GET',
                path='/new-match',
                params={},
                body={
                    'first_player_name' : 'Victor',
                    'second_player_name' : 'Dmitriy'
                }
            )
        )
        assert response.status == HTTPStatus.SEE_OTHER

    def test_create_match_unknown_players(self, match_controller: MatchController) -> None:
        response = match_controller.create_match(
            HttpRequest(
                method='GET',
                path='/new-match',
                params={},
                body={
                    'first_player_name' : 'Sergey',
                    'second_player_name' : 'Jukov'
                }
            )
        )
        assert response.status == HTTPStatus.SEE_OTHER

    def test_create_match_without_params(self, match_controller: MatchController) -> None:
        response = match_controller.create_match(
            HttpRequest(
                method='GET',
                path='/new-match',
                params={},
                body={
                }
            )
        )
        assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_update_match(self, match_controller: MatchController, fill_matches) -> None:
        response = match_controller.update_match(
            HttpRequest(
                method='GET',
                path='/match-score?uuid=',
                params={
                    'uuid' : '00000000-0000-0000-0000-0000-00000001',
                },
                body={
                    'score_to_change' : 'first_player_score'
                }
            )
        )
        assert response.status == HTTPStatus.OK

    def test_update_unexisting_match(self, match_controller: MatchController) -> None:
        response = match_controller.update_match(
            HttpRequest(
                method='GET',
                path='/match-score?uuid=',
                params={
                    'uuid' : '00000000-0000-0000-0000-0000-00000001',
                },
                body={
                    'score_to_change' : 'first_player_score'
                }
            )
        )
        assert response.status == HTTPStatus.NOT_FOUND

    def test_update_ended_match(self, match_controller: MatchController, fill_matches) -> None:
        response = match_controller.update_match(
            HttpRequest(
                method='GET',
                path='/match-score?uuid=',
                params={
                    'uuid' : '00000000-0000-0000-0000-0000-00000002',
                },
                body={
                    'score_to_change' : 'first_player_score'
                }
            )
        )
        assert response.status == HTTPStatus.IM_A_TEAPOT