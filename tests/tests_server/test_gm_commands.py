import pytest


@pytest.mark.asyncio
async def test_gm_force_move(valid_character, custom_room, gm_client):
    source_room = valid_character.room
    target_room = custom_room('move_room', 'IC Room Test', 'For IC testing')

    moving_char = valid_character

    data_in = [{
        'command': 'gmforcemove',
        'character': moving_char.short_name,
        'target_room': target_room.short_name
    }]

    ooc_name = 'gm ooc name'
    client = gm_client(ooc_name, data_in)

    assert moving_char in source_room.characters
    assert moving_char not in target_room.characters

    await client.handle()

    assert moving_char not in source_room.characters
    assert moving_char in target_room.characters

    data_out = [{
        'command': 'gmcharmove',
        'gm_ooc_name': ooc_name,
        'character': moving_char.short_name,
        'source_room': source_room.short_name,
        'target_room': target_room.short_name,
        'was_forced': True
    }]

    assert client.socket.has_equal_output(data_out)
