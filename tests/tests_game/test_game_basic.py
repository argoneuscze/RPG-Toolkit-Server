from game.game import Game


def test_game_io(tmpdir, game):
    directory = tmpdir.mkdir("game")
    filename = directory + "game.dat"
    game.save_game(filename)
    new_game = Game.load_game(filename)
    assert new_game == game
