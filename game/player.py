from server.player_interface import PlayerInterface


class Player(PlayerInterface):
    def __init__(self, name, client, is_gm):
        self.ooc_name = name
        self.client = client
        self.is_gm = is_gm
