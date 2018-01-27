from server.player_interface import PlayerInterface


class Player(PlayerInterface):
    def __init__(self, client, ooc_name, is_gm):
        self.ooc_name = ooc_name
        self.client = client
        self.is_gm = is_gm

    def send_auth_ok(self):
        self.client.send_auth_ok()

    def send_room_info(self, room):
        self.client.send_room_info(room)
