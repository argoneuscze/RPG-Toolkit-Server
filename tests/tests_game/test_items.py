from game.character import Character
from game.item import ItemTemplate, Item, ItemContainer
from game.room import Room


def test_item_transfer():
    bp_t = ItemTemplate('backpack', 'A backpack', 'N/A', True)
    bp2_t = ItemTemplate('backpack2', 'Another backpack', 'N/A', True)
    k_t = ItemTemplate('key', 'A key', 'N/A', False)

    # create a backpack (1) with a key (1) in it
    bp_1 = ItemContainer(bp_t)
    k_1 = Item(k_t)
    bp_1.add_item(k_1)

    # create another backpack (2)
    bp_2 = ItemContainer(bp_t)

    # create another backpack (3) with another key (2) in it
    bp_3 = ItemContainer(bp2_t)
    k_2 = Item(k_t)
    bp_3.add_item(k_2)

    # create a room
    r_1 = Room('room', 'room')

    # create a character and give him backpacks (1) and (3)
    c_1 = Character('transferer', '', '', r_1)
    c_1.items.add_item(bp_1)
    c_1.items.add_item(bp_3)

    # create a character and give him backpack (2)
    c_2 = Character('transferee', '', '', r_1)
    c_2.items.add_item(bp_2)

    # move backpack (1) with key (1) to other character
    assert bp_1 in c_1.items
    assert bp_1 not in c_2.items

    c_1.items.transfer_item(bp_1.get_short_name(), c_2.items)

    assert bp_1 not in c_1.items
    assert bp_1 in c_2.items

    # indirectly move key (2) from character's backpack (3) to other character
    assert k_2 in bp_3
    assert k_2 not in c_2.items

    c_1.items.transfer_item(k_2.get_short_name(), c_2.items)

    assert k_2 not in bp_3
    assert k_2 in c_2.items
