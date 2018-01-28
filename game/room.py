class Room:
    def __init__(self, short_name, long_name, description='N/A'):
        self.characters = set()
        self.short_name = short_name
        self.long_name = long_name
        self.description = description
        self.adjacent_rooms = set()

    def add_character(self, char):
        self.characters.add(char)

    def remove_character(self, char):
        self.characters.remove(char)

    def set_description(self, description):
        self.description = description

    def as_dict(self):
        data = {
            'short_name': self.short_name,
            'long_name': self.long_name,
            'description': self.description,
            'adjacent': [room.short_name for room in self.adjacent_rooms]
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

    def __eq__(self, other):
        return self.characters == other.characters and \
               self.short_name == other.short_name and \
               self.long_name == other.long_name and \
               len(self.adjacent_rooms) == len(other.adjacent_rooms) and \
               self.description == other.description

    def __hash__(self):
        return hash((self.short_name, self.long_name, self.description))
