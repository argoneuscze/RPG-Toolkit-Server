class Character:
    def __init__(self, short_name, full_name, password, room):
        self.short_name = short_name
        self.full_name = full_name
        self.password = password
        self.room = room
        self.players = set()

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.remove(player)

    def set_password(self, password):
        self.password = password

    def as_dict(self):
        # TODO more
        data = {
            'name': self.short_name
        }
        return data
