from game.character_manager import CharacterManager
from game.room_manager import RoomManager


class Game:
    def __init__(self):
        self.char_manager = CharacterManager()
        self.room_manager = RoomManager()

    def new_player(self, player, password):
        """
        Adds a new player client to the current game.

        Args:
            player (PlayerInterface): The player to be added
            password (str): A password for a character

        """
        self.char_manager.auth_player(player, password)

    @staticmethod
    def load_game(filename):
        ...

    def save_game(self, filename):
        ...

    def __eq__(self, other):
        ...
