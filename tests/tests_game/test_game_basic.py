def test_game_io(basic_game, empty_game):
    basic_game.save_game(basic_game.gamedir)
    empty_game.load_game(basic_game.gamedir)
    assert basic_game == empty_game
