import json

from game.character import Character


class CharacterManager:
    def __init__(self):
        self.characters = dict()

    def get_char_by_password(self, password):
        for _, char in self.characters.items():
            if char.password == password:
                return char
        return None

    def get_char(self, short_name):
        return self.characters.get(short_name)

    def load_characters(self, gamedir, rooms, item_manager):
        data = json.load(open("{}/characters.json".format(gamedir)))
        for char in data:
            room = rooms[char['room']]
            c = Character(char['short_name'], char['full_name'], char['password'], room)
            for item in item_manager.construct_loaded_items(char['items']):
                c.items.add_item(item)
            self.characters[char['short_name']] = c

    def save_characters(self, gamedir):
        with open('{}/characters.json'.format(gamedir), 'w') as outfile:
            json.dump([char.as_dict() for char in self.characters.values()], outfile)

    def __eq__(self, other):
        return self.characters == other.characters
