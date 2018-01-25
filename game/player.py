from server.player_interface import PlayerInterface


class Player(PlayerInterface):
    def __init__(self, client, ooc_name, is_gm):
        self.ooc_name = ooc_name
        self.client = client
        self.is_gm = is_gm
