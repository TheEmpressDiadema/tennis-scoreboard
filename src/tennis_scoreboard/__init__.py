import waitress

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tennis_scoreboard.app.wsgi import WsgiApp
from tennis_scoreboard.app.router import Router
from tennis_scoreboard.views.renderer import Renderer
from tennis_scoreboard.core.db_config import DBConfig
from tennis_scoreboard.repositories.unit_of_work import UnitOfWork
from tennis_scoreboard.services.match_service import MatchService
from tennis_scoreboard.services.score_service import ScoreService
from tennis_scoreboard.controllers.match_controller import MatchController
from tennis_scoreboard.controllers.static_controller import StaticController
from tennis_scoreboard.controllers.static_html_controller import StaticHtmlController

def build_app():
    engine = create_engine(DBConfig.get_database_url('db_config.toml', 'server_security.toml'))
    controller = MatchController(
        MatchService(
            UnitOfWork(
                sessionmaker(engine)
            )
        ),
        ScoreService()
    )
    html_controller = StaticHtmlController()
    static_controller = StaticController()
    router = Router()
    router.register_route('GET', '/', html_controller.get_start_page)
    router.register_route('GET', '/new-match', html_controller.get_new_match_page)
    router.register_route('GET', '/matches', controller.get_matches)
    router.register_route('GET', '/match-score', controller.get_match)
    router.register_route('POST', '/new-match', controller.create_match)
    router.register_route('POST', '/match-score', controller.update_match)
    router.register_route('GET', '/static/styles.css', static_controller.get_css)
    router.register_route('GET', '/favicon.ico', static_controller.get_empty_favicon)
    renderer = Renderer()
    app = WsgiApp(router, renderer)
    return app

def main() -> None:
    app = build_app()
    waitress.serve(app, host='127.0.0.1', port=8080, threads=1)