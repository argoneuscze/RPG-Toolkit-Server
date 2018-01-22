from server.player_interface import PlayerInterface


class Character(PlayerInterface):
    def __init__(self):
        self.password = None
        self.players = set()

    def add_player(self, client):
        self.players.add(client)

    def remove_player(self, client):
        self.players.remove(client)

    def set_password(self, password):
        self.password = password
