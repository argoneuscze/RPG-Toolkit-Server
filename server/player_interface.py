from abc import ABC


class PlayerInterface(ABC):
    def send_auth_ok(self):
        raise NotImplementedError

    def send_auth_failure(self, message):
        raise NotImplementedError

    def send_message_ic(self, char_from, message):
        raise NotImplementedError

    def send_message_ooc(self, player_from, message):
        raise NotImplementedError

    def send_room_info(self, room):
        raise NotImplementedError

    def send_character_left_room(self, character, room, verbose):
        raise NotImplementedError

    def send_character_entered_room(self, character, room, verbose):
        raise NotImplementedError

    def send_gm_character_moved(self, player, character, source_room, target_room, force):
        raise NotImplementedError
