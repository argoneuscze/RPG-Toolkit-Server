import json


class CharacterManager:
    def __init__(self, room_manager):
        self.room_manager = room_manager
        self.characters = []
        self.load_characters()

    def get_char_by_password(self, password):
        for char in self.characters:
            if char.password == password:
                return char
        return None

    def load_characters(self):
        try:
            data = json.load(open("config/characters.json"))
        except FileNotFoundError:
            return
        # TODO actually load
        print(data)

    def save_characters(self):
        with open('config/characters.json', 'w') as outfile:
            json.dump([char.as_dict() for char in self.characters], outfile)
