import pytest

from tests.utils import get_engine
from tennis_scoreboard.models.models import (
    BaseModel,
    Player,
    Match
)

@pytest.fixture(scope='session', autouse=True)
def prepare_database() -> None:
    engine = get_engine()
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)