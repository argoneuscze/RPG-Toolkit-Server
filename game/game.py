from game.character_manager import CharacterManager
from game.player_manager import PlayerManager
from game.room_manager import RoomManager


class Game:
    def __init__(self):
        self.room_manager = RoomManager()
        self.char_manager = CharacterManager(self.room_manager)
        self.player_manager = PlayerManager(self.char_manager)

    def new_player_character(self, client, password, ooc_name):
        """
        Adds a new player client to the current game.

        Args:
            client: The client to be added as a new Player
            password (str): A password for a character
            ooc_name (str): The name of the player

        """
        self.player_manager.auth_client_player(client, password, ooc_name)

    def new_player_gm(self, client, password, ooc_name):
        self.player_manager.auth_client_gm(client, password, ooc_name)

    def remove_client(self, client):
        ...

    @staticmethod
    def load_game(filename):
        ...

    def save_game(self, filename):
        ...

    def __eq__(self, other):
        ...
