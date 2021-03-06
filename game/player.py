from server.player_interface import PlayerInterface


class Player(PlayerInterface):
    """This class represents a Player inside the Game, either as a Game master or as a Character player.

    A Player is a generic concept that's native to the Game itself, independent
    on the specifics of interacting with them, for example over network.

    The class implements the PlayerInterface, responsible for communication with the actual client.

    """

    def __init__(self, client, ooc_name, is_gm):
        self.ooc_name = ooc_name
        self.client = client
        self.is_gm = is_gm

    def send_auth_ok(self):
        self.client.send_auth_ok()

    def send_auth_failure(self, message):
        self.client.send_auth_failure(message)

    def send_room_info(self, room):
        self.client.send_room_info(room)

    def send_message_ic(self, char_from, message):
        self.client.send_message_ic(char_from, message)

    def send_message_ooc(self, player_from, message):
        self.client.send_message_ooc(player_from, message)

    def send_character_left_room(self, character, room, verbose=True):
        self.client.send_character_left_room(character, room, verbose)

    def send_character_entered_room(self, character, room, verbose=True):
        self.client.send_character_entered_room(character, room, verbose)

    def send_gm_character_moved(self, gm, character, source_room, target_room, force=False):
        self.client.send_gm_character_moved(gm, character, source_room, target_room, force)
