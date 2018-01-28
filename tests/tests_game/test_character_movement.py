from game.room import Room


def test_move_adjacent_room(valid_character):
    source_room = valid_character.room
    target_room = next(iter(source_room.adjacent_rooms))

    res = valid_character.move_to_room(target_room)

    assert res
    assert valid_character not in source_room.characters
    assert valid_character in target_room.characters
    assert valid_character.room == target_room


def test_move_inadjacent_room(valid_character):
    source_room = valid_character.room
    disjointed_room = Room('inadj', 'Inadjacent room')

    res = valid_character.move_to_room(disjointed_room)

    assert not res
    assert valid_character in source_room.characters
    assert valid_character not in disjointed_room.characters
    assert valid_character.room == source_room
