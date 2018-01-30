import pytest

from tests.tests_server.conftest import room_to_json


@pytest.mark.asyncio
async def test_player_auth(new_client, valid_character):
    room = valid_character.room
    password = valid_character.password

    data_in = [{
        'command': 'identplayer',
        'password': password,
        'ooc_name': 'test_name'
    }]

    data_out = [
        {
            'command': 'auth_ok'
        },
        room_to_json(room, True)
    ]

    print(data_out)

    client = new_client(data_in)
    await client.handle()

    assert client.socket.has_equal_output(data_out)


@pytest.mark.asyncio
async def test_player_auth_invalidpass(new_client):
    password = 'invalid_pass'

    data_in = [{
        'command': 'identplayer',
        'password': password,
        'ooc_name': 'test_name'
    }]

    data_out = [{
        'command': 'auth_failure',
        'message': 'Invalid password.'
    }]

    client = new_client(data_in)
    await client.handle()

    assert client.socket.has_equal_output(data_out)


@pytest.mark.asyncio
async def test_gm_auth(basic_game, new_client):
    valid_pass = next(iter(basic_game.player_manager.gm_passwords))

    room_data = []

    for room in basic_game.room_manager.rooms.values():
        room_data.append(room_to_json(room))

    data_in = [{
        'command': 'identgm',
        'password': valid_pass,
        'ooc_name': 'test_gm_name'
    }]

    data_out = [
        {
            'command': 'auth_ok'
        },
        {
            'command': 'roomlist',
            'rooms': room_data
        }]

    client = new_client(data_in)
    await client.handle()

    assert client.socket.has_equal_output(data_out)
