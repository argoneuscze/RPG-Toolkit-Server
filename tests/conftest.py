import pytest

from game.game import Game


@pytest.fixture
def game():
    g = Game()
    return g
