import json

import pytest

from game.character import Character
from game.game import Game
from game.room import Room
from server.run_server import Server


@pytest.fixture
def empty_game():
    g = Game()
    return g


@pytest.fixture
def basic_game(tmpdir):
    g = Game()
    g.gamedir = tmpdir.mkdir("test_game")
    with open('{}/gm_passwords.json'.format(g.gamedir), 'w') as outfile:
        json.dump({'passwords': ['gmpass1', 'gmpass2']}, outfile)
    g.player_manager.load_gm_passwords(g.gamedir)
    room1 = Room('room1', 'Room #1', 'First room.')
    room2 = Room('room2', 'Room #2', 'Second room.')
    room3 = Room('room3', 'Room #3', 'Third room.')
    room1.adjacent_rooms.add(room2)
    room2.adjacent_rooms.add(room1)
    room2.adjacent_rooms.add(room3)
    room3.adjacent_rooms.add(room2)
    room3.adjacent_rooms.add(room1)
    char1 = Character('char1', 'First Character', '1234', room1)
    char2 = Character('char2', 'Second Character', 'qwerty', room3)
    g.room_manager.rooms['room1'] = room1
    g.room_manager.rooms['room2'] = room2
    g.room_manager.rooms['room3'] = room3
    g.char_manager.characters['char1'] = char1
    g.char_manager.characters['char2'] = char2
    return g


@pytest.fixture
def valid_character(basic_game):
    return next(iter(basic_game.char_manager.characters.values()))


@pytest.fixture
def custom_character(basic_game):
    def construct_character(short_name, full_name, password, room):
        c = Character(short_name, full_name, password, room)
        basic_game.char_manager.characters[short_name] = c
        return c

    return construct_character


@pytest.fixture()
def server(game):
    s = Server(game)
    return s
