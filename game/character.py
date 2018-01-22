class Character:
    def __init__(self):
        self.password = None
        self.players = set()

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        self.players.remove(player)

    def set_password(self, password):
        self.password = password
