import json

from game.room import Room


class RoomManager:
    """Manager responsible for loading and saving rooms."""

    def __init__(self):
        self.rooms = dict()

    def load_rooms(self, gamedir, item_manager):
        data = json.load(open("{}/rooms.json".format(gamedir)))
        for room in data:
            r = Room(room['short_name'], room['long_name'], room['description'])
            for item in item_manager.construct_loaded_items(room['items']):
                r.items.add_item(item)
            self.rooms[room['short_name']] = r
        for room in data:
            for adj in room['adjacent']:
                self.rooms[room['short_name']].adjacent_rooms.add(self.rooms[adj])

    def save_rooms(self, gamedir):
        with open('{}/rooms.json'.format(gamedir), 'w') as outfile:
            json.dump([room.as_dict() for room in self.rooms.values()], outfile)

    def get_rooms(self):
        return self.rooms.values()

    def __eq__(self, other):
        return self.rooms == other.rooms
