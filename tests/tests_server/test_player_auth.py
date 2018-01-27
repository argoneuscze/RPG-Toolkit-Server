import pytest


@pytest.mark.asyncio
async def test_player_auth(new_client, valid_character):
    room = valid_character.room
    password = valid_character.password
    expected_characters = []

    for char in room.characters:
        expected_characters.append({
            'short_name': char.short_name,
            'full_name': char.full_name
        })

    data_in = [{
        'command': 'identplayer',
        'password': password,
        'ooc_name': 'test_name'
    }]

    data_out = [
        {
            'command': 'auth_ok'
        },
        {
            'command': 'roominfo',
            'room_short_name': room.short_name,
            'room_long_name': room.long_name,
            'room_description': room.description,
            'characters': expected_characters
        }
    ]

    client = new_client(data_in)
    await client.handle()

    assert client.socket.has_equal_output(data_out)


@pytest.mark.asyncio
async def test_player_auth_invalidpass(new_client, valid_character):
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
