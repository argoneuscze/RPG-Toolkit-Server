class Character:
    def __init__(self, short_name, full_name, password, room):
        self.short_name = short_name
        self.full_name = full_name
        self.password = password
        self.room = room
        self.players = set()

        self.room.add_character(self)

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.remove(player)

    def set_password(self, password):
        self.password = password

    def as_dict(self):
        data = {
            'short_name': self.short_name,
            'full_name': self.full_name,
            'password': self.password,
            'room': self.room.short_name
        }
        return data

    def __eq__(self, other):
        return self.short_name == other.short_name and \
               self.full_name == other.full_name and \
               self.password == other.password and \
               self.room.short_name == other.room.short_name

    def __hash__(self):
        return hash((self.short_name, self.full_name, self.password))
