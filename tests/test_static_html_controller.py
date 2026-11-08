
from http import HTTPStatus

from tennis_scoreboard.controllers.static_html_controller import StaticHtmlController
from tennis_scoreboard.controllers.structures import HttpRequest


class TestStaticHtmlController:

    def test_get_main_page(self):
        controller = StaticHtmlController()
        response = controller.get_main_page(
            HttpRequest(
                method='GET',
                path='/',
                params={},
                body={}
            )
        )
        assert response.status == HTTPStatus.OK

    def test_get_new_match_page(self):
        controller = StaticHtmlController()
        response = controller.get_new_match_page(
            HttpRequest(
                method='GET',
                path='/new-match',
                params={},
                body={}
            )
        )
        assert response.status == HTTPStatus.OK