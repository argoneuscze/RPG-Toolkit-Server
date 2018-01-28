import asyncio

import pytest


@pytest.mark.asyncio
async def test_move_adjacent_room_server(player_client, valid_character, custom_character, custom_room):
    source_room = valid_character.room
    target_room = next(iter(source_room.adjacent_rooms))
    another_room = custom_room('move_room', 'IC Room Test', 'For IC testing')

    moving_char = valid_character
    see_leaving_char = custom_character('move_char', 'Move Test', 'icpass', source_room)
    see_entering_char = custom_character('move_char2', 'Move Test 2', 'icpass2', target_room)
    another_char = custom_character('move_char3', 'IC Char Test 2', 'icpass3', another_room)

    data_in = [{
        'command': 'playermove',
        'target_room': target_room.short_name
    }]

    client_moving = player_client(moving_char, 'client moving', data_in)
    client_see_leaving = player_client(see_leaving_char, 'client seeing leaving', [])
    client_see_entering = player_client(see_entering_char, 'client seeing entering', [])
    client_unrelated = player_client(another_char, 'client unrelated', [])

    client_moving.socket.set_wait_delay(2)
    client_see_leaving.socket.set_wait_delay(2)
    client_see_entering.socket.set_wait_delay(2)
    client_unrelated.socket.set_wait_delay(2)

    await asyncio.gather(client_moving.handle(), client_see_leaving.handle(),
                         client_see_entering.handle(), client_unrelated.handle())

    target_room_chars = []
    for char in target_room.characters:
        target_room_chars.append({
            'short_name': char.short_name,
            'full_name': char.full_name
        })

    data_out_moving = [{
        'command': 'roominfo',
        'room_short_name': target_room.short_name,
        'room_long_name': target_room.long_name,
        'room_description': target_room.description,
        'adjacent_rooms': [{'short_name': room.short_name, 'long_name': room.long_name}
                           for room in target_room.adjacent_rooms],
        'characters': target_room_chars
    }]

    data_out_see_leaving = [{
        'command': 'charleave',
        'char_short_name': moving_char.short_name,
        'char_full_name': moving_char.full_name,
        'room_to_short_name': target_room.short_name,
        'room_to_long_name': target_room.short_name
    }]

    data_out_see_entering = [{
        'command': 'charenter',
        'char_short_name': moving_char.short_name,
        'char_full_name': moving_char.full_name,
        'room_from_short_name': source_room.short_name,
        'room_from_long_name': source_room.short_name
    }]

    assert client_moving.socket.has_equal_output(data_out_moving)
    assert client_see_leaving.socket.has_equal_output(data_out_see_leaving)
    assert client_see_entering.socket.has_equal_output(data_out_see_entering)
    assert client_unrelated.socket.has_equal_output([])
