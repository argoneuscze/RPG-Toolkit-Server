import pytest

from game.game import Game
from server.run_server import Server


@pytest.fixture
def game():
    g = Game()
    return g


@pytest.fixture()
def server(game):
    s = Server(game)
    return s
