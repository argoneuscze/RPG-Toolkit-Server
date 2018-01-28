import asyncio

import pytest

from game.room import Room


@pytest.mark.asyncio
async def test_message_ic(player_client, valid_character, custom_character):
    msg = 'This is a test message.'
    data_in = [{
        'command': 'messageic',
        'message': msg
    }]
    data_out = [{
        'command': 'messageic',
        'character_short_name': valid_character.short_name,
        'character_full_name': valid_character.full_name,
        'message': msg
    }]

    room = valid_character.room
    another_room = Room('ic_room', 'IC Room Test', 'For IC testing')

    receiving_char = custom_character('ic_char', 'IC Char Test', 'icpass', room)
    another_char = custom_character('ic_char2', 'IC Char Test 2', 'icpass2', another_room)

    client_sender = player_client(valid_character, 'client one', data_in)
    client_receiver = player_client(receiving_char, 'client two', [])
    client_unrelated = player_client(another_char, 'client unrelated', [])

    client_sender.socket.set_wait_delay(1)
    client_receiver.socket.set_wait_delay(1)
    client_unrelated.socket.set_wait_delay(1)

    await asyncio.gather(client_sender.handle(), client_receiver.handle(), client_unrelated.handle())

    assert client_sender.socket.has_equal_output(data_out)
    assert client_receiver.socket.has_equal_output(data_out)
    assert client_unrelated.socket.has_equal_output([])


@pytest.mark.asyncio
async def test_message_ooc(player_client, valid_character, custom_character):
    msg = 'This is a test message.'
    ooc_name = 'client one'

    data_in = [{
        'command': 'messageooc',
        'message': msg
    }]

    room = valid_character.room
    another_room = Room('ic_room', 'IC Room Test', 'For IC testing')

    receiving_char = custom_character('ic_char', 'IC Char Test', 'icpass', room)
    another_char = custom_character('ic_char2', 'IC Char Test 2', 'icpass2', another_room)

    client_sender = player_client(valid_character, ooc_name, data_in)
    client_receiver = player_client(receiving_char, 'client two', [])
    client_unrelated = player_client(another_char, 'client unrelated', [])

    data_out = [{
        'command': 'messageooc',
        'player_name': ooc_name,
        'message': msg
    }]

    client_sender.socket.set_wait_delay(1)
    client_receiver.socket.set_wait_delay(1)
    client_unrelated.socket.set_wait_delay(1)

    await asyncio.gather(client_sender.handle(), client_receiver.handle(), client_unrelated.handle())

    assert client_sender.socket.has_equal_output(data_out)
    assert client_receiver.socket.has_equal_output(data_out)
    assert client_unrelated.socket.has_equal_output([])
