from server.player_interface import PlayerInterface


class Character(PlayerInterface):
    def __init__(self):
        self.players = set()

    def new_player(self, client):
        self.players.add(client)

    def remove_player(self, client):
        self.players.remove(client)
