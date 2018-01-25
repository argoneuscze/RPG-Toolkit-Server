class Character:
    def __init__(self, room):
        self.password = None
        self.players = set()
        self.room = room

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.remove(player)

    def set_password(self, password):
        self.password = password
