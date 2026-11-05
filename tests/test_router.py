import pytest

from http import HTTPStatus
from tennis_scoreboard.app.router import Router
from tennis_scoreboard.controllers.structures import HttpRequest

class TestRouter:

    def test_found_route(self, router: Router, fill_matches) -> None:
        handler = router.get_handler('get', 'matches')
        response = handler(
            HttpRequest(
                method='GET',
                path='/matches',
                params={},
                body={}
            )
        )
        assert response.status == HTTPStatus.OK

    def test_route_not_found(self, router: Router) -> None:
        with pytest.raises(LookupError):
            handler = router.get_handler('GET', 'masdasd')