from abc import ABC


class PlayerInterface(ABC):
    def send_auth_ok(self):
        raise NotImplementedError

    def send_auth_failure(self, message):
        raise NotImplementedError

    def send_ic_message(self, char_from, message):
        raise NotImplementedError

    def send_ooc_message(self, player_from, message):
        raise NotImplementedError

    def send_room_info(self, room):
        raise NotImplementedError

    def send_character_left_room(self, character, target_room):
        raise NotImplementedError

    def send_character_entered_room(self, character, target_room):
        raise NotImplementedError
