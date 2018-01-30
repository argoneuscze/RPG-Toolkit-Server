import sys

from game.character_manager import CharacterManager
from game.item_manager import ItemManager
from game.log import GameLog
from game.player_manager import PlayerManager
from game.room_manager import RoomManager


class Game:
    def __init__(self):
        self.item_manager = ItemManager()
        self.room_manager = RoomManager()
        self.char_manager = CharacterManager()
        self.player_manager = PlayerManager(self.char_manager)
        self.gamedir = None
        self.log = GameLog()

    def load_game(self, gamedir):
        self.gamedir = gamedir
        self.log.open_file(gamedir, 'action.log')
        try:
            self.item_manager.load_item_templates(gamedir)
            self.player_manager.load_gm_passwords(gamedir)
            self.room_manager.load_rooms(gamedir, self.item_manager)
            rooms = self.room_manager.rooms
            self.char_manager.load_characters(gamedir, rooms, self.item_manager)
        except FileNotFoundError:
            print('Could not load game, important files missing.')
            sys.exit(1)

    def save_game(self, gamedir=''):
        if not gamedir:
            gamedir = self.gamedir
        self.room_manager.save_rooms(gamedir)
        self.char_manager.save_characters(gamedir)
        self.item_manager.save_item_templates(gamedir)

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
        player = self.player_manager.auth_client_gm(client, password, ooc_name)
        if player is None:
            client.send_auth_failure('Invalid password.')
            return
        player.send_auth_ok()
        for room in self.room_manager.get_rooms():
            player.send_room_info(room)

    def remove_client(self, client):
        self.player_manager.remove_player(client)

    def message_ic(self, client, message):
        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        character.room.send_message_ic(character, message)
        self.log.log_message_ic(character, message)

    def message_ooc(self, client, message):
        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        character.room.send_message_ooc(player, message)
        self.log.log_message_ooc(character, player, message)

    def move_player(self, client, target_room_str):
        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        source_room = character.room
        target_room = self.room_manager.rooms[target_room_str]
        if character.move_to_room(target_room):
            player.send_room_info(target_room)
            target_room.send_character_entered(character, source_room)
            source_room.send_character_left(character, target_room)
            self.log.log_player_action(player, '{} moved from room {} to room {}'.format(
                character.full_name, source_room.long_name, target_room.long_name))

    def __eq__(self, other):
        return self.room_manager == other.room_manager and \
               self.char_manager == other.char_manager and \
               self.item_manager == other.item_manager and \
               self.player_manager == other.player_manager
