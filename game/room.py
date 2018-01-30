from game.item import GenericContainer


class Room:
    def __init__(self, short_name, long_name, description='N/A'):
        self.characters = set()
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.adjacent_rooms = set()
        self.items = GenericContainer()

    def add_character(self, char):
        self.characters.add(char)

    def remove_character(self, char):
        self.characters.remove(char)

    def set_description(self, description):
        self.description = description

    def is_adjacent(self, room):
        return room in self.adjacent_rooms

    def as_dict(self):
        data = {
            'short_name': self.short_name,
            'long_name': self.long_name,
            'description': self.description,
            'adjacent': [room.short_name for room in self.adjacent_rooms],
            'items': self.items.as_list()
        }
        return data

    def send_message_ic(self, char_from, message):
        for char in self.characters:
            for player in char.players:
                player.send_message_ic(char_from, message)

    def send_message_ooc(self, player_from, message):
        for char in self.characters:
            for player in char.players:
                player.send_message_ooc(player_from, message)

    def send_character_left(self, character, target_room, verbose=True):
        for char in self.characters:
            if char == character:
                continue
            for player in char.players:
                player.send_character_left_room(character, target_room, verbose)

    def send_character_entered(self, character, source_room, verbose=True):
        for char in self.characters:
            if char == character:
                continue
            for player in char.players:
                player.send_character_entered_room(character, source_room, verbose)

    def __eq__(self, other):
        return self.characters == other.characters and \
               self.short_name == other.short_name and \
               self.long_name == other.long_name and \
               len(self.adjacent_rooms) == len(other.adjacent_rooms) and \
               self.description == other.description and \
               self.items == other.items

    def __hash__(self):
        return hash((self.short_name, self.long_name, self.description))
