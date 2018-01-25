from game.character_manager import CharacterManager
from game.player_manager import PlayerManager
from game.room_manager import RoomManager


class Game:
    def __init__(self):
        self.char_manager = CharacterManager()
        self.room_manager = RoomManager()
        self.player_manager = PlayerManager(self.char_manager)

    def new_player_character(self, client, password):
        """
        Adds a new player client to the current game.

        Args:
            client: The client to be added as a new Player
            password (str): A password for a character

        """
        self.player_manager.auth_client_player(client, password)

    def new_player_gm(self, client, password):
        self.player_manager.auth_client_gm(client, password)

    def remove_client(self, client):
        ...

    @staticmethod
    def load_game(filename):
        ...

    def save_game(self, filename):
        ...

    def __eq__(self, other):
        ...
