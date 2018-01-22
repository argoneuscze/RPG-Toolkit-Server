from abc import ABC


class PlayerInterface(ABC):
    def send_ic_message(self, char_from, message):
        raise NotImplementedError
