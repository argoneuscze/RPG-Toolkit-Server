import sys

from game.character_manager import CharacterManager
from game.player_manager import PlayerManager
from game.room_manager import RoomManager


class Game:
    def __init__(self):
        self.room_manager = RoomManager()
        self.char_manager = CharacterManager()
        self.player_manager = PlayerManager(self.char_manager)
        self.gamedir = '.'

    def load_game(self, gamedir):
        self.gamedir = gamedir
        try:
            self.player_manager.load_gm_passwords(gamedir)
            self.room_manager.load_rooms(gamedir)
            rooms = self.room_manager.rooms
            self.char_manager.load_characters(gamedir, rooms)
        except FileNotFoundError:
            print('Could not load game, important files missing.')
            sys.exit(1)

    def save_game(self, gamedir=''):
        if not gamedir:
            gamedir = self.gamedir
        self.room_manager.save_rooms(gamedir)
        self.char_manager.save_characters(gamedir)

    def new_player_character(self, client, password, ooc_name):
        """
        Adds a new player client to the current game.

        Args:
            client: The client to be added as a new Player
            password (str): A password for a character
            ooc_name (str): The name of the player

        """
        player, character = self.player_manager.auth_client_player(client, password, ooc_name)
        if player is None:
            client.send_auth_failure('Invalid password.')
            return
        player.send_auth_ok()
        player.send_room_info(character.room)

    def new_player_gm(self, client, password, ooc_name):
        self.player_manager.auth_client_gm(client, password, ooc_name)

    def remove_client(self, client):
        self.player_manager.remove_player(client)

    def message_ic(self, client, message):
        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        character.room.send_message_ic(character, message)

    def __eq__(self, other):
        return self.room_manager == other.room_manager and \
               self.char_manager == other.char_manager and \
               self.player_manager == other.player_manager
