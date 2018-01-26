class Room:
    def __init__(self, short_name, long_name, description='N/A'):
        self.characters = set()
        self.short_name = short_name
        self.long_name = long_name
        self.description = description

    def add_character(self, char):
        self.characters.add(char)

    def remove_character(self, char):
        self.characters.remove(char)

    def set_description(self, description):
        ...

    def as_dict(self):
        data = {
            'short_name': self.short_name,
            'long_name': self.long_name,
            'description': self.description
        }
        return data

    def __eq__(self, other):
        return self.characters == other.characters and \
               self.short_name == other.short_name and \
               self.long_name == other.long_name and \
               self.description == other.description

    def __hash__(self):
        return hash((self.short_name, self.long_name, self.description))
