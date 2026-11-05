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

def main() -> None:
    engine = create_engine(DBConfig.get_database_url('db_config.toml', 'server_security.toml'))
    controller = MatchController(
        MatchService(
            UnitOfWork(
                sessionmaker(engine)
            )
        ),
        ScoreService()
    )
    router = Router()
    router.register_route('GET', '/', controller.get_start_page)
    router.register_route('GET', '/new-match', controller.get_create_match_page)
    router.register_route('GET', '/matches', controller.get_matches)
    router.register_route('GET', '/match-score', controller.get_match)
    renderer = Renderer()
    app = WsgiApp(router, renderer)
    waitress.serve(app, listen='127.0.0.1:8080')

main()