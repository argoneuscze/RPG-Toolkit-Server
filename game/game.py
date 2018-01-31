import sys

from game.character_manager import CharacterManager
from game.item_manager import ItemManager
from game.log import GameLog
from game.player_manager import PlayerManager
from game.room_manager import RoomManager


class Game:
    """This class represents the actual Game where everything takes place"""

    def __init__(self):
        self.item_manager = ItemManager()
        self.room_manager = RoomManager()
        self.char_manager = CharacterManager()
        self.player_manager = PlayerManager(self.char_manager)
        self.gamedir = None
        self.log = GameLog()

    def load_game(self, gamedir):
        """Loads a game from a given directory"""

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
        print('Game loaded.')

    def save_game(self, gamedir=''):
        """Saves the game to the current game's directory."""

        if not gamedir:
            gamedir = self.gamedir
        self.room_manager.save_rooms(gamedir)
        self.char_manager.save_characters(gamedir)
        self.item_manager.save_item_templates(gamedir)
        print('Game saved.')

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
        """This function is called when a new player tries to join as a GM. See new_player_character."""

        player = self.player_manager.auth_client_gm(client, password, ooc_name)
        if player is None:
            client.send_auth_failure('Invalid password.')
            return
        player.send_auth_ok()
        for room in self.room_manager.get_rooms():
            player.send_room_info(room)

    def remove_client(self, client):
        """Called when a player disconnects, this removes them from the Game."""

        self.player_manager.remove_player(client)

    def message_ic(self, client, message):
        """Called when a player sends an IC (In Character) message.

        Sends a message to every other character in the same room as the sender's character.

        """

        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        character.room.send_message_ic(character, message)
        self.log.log_message_ic(character, message)

    def message_ooc(self, client, message):
        """Called when a player sends an OOC (Out of Character) message.

        Same as message_ic, except they send it with the player's identity, not the character's.

        """

        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        character.room.send_message_ooc(player, message)
        self.log.log_message_ooc(character, player, message)

    def move_player(self, client, target_room_str):
        """Called when a player tries to move their character to another room.

        For this to work, the target room needs to be adjacent to the current one.
        This also notifies the characters in each room and the GMs about said movement.

        """

        player, character = self.player_manager.get_player(client)
        if character is None:
            raise PermissionError('You need to be authorized as a player to do that')
        source_room = character.room
        target_room = self.room_manager.rooms[target_room_str]
        if character.move_to_room(target_room):
            player.send_room_info(target_room)
            target_room.send_character_entered(character, source_room)
            source_room.send_character_left(character, target_room)
            for gm in self.player_manager.gamemasters:
                gm.send_gm_character_moved(player, character, source_room, target_room, False)
            self.log.log_player_action(player, '{} moved from room {} to room {}'.format(
                character.full_name, source_room.long_name, target_room.long_name))

    def gm_move_character(self, client, char_name, target_room_str):
        """Called when a GM tries to forcibly move a character to another room.

        Target room does not need to be adjacent in this case, nor do the characters get notified.

        """

        player = self.player_manager.get_gm(client)
        if player is None:
            raise PermissionError('You need to be authorized as a GM to do that')
        character = self.char_manager.get_char(char_name)
        source_room = character.room
        target_room = self.room_manager.rooms[target_room_str]
        if character.move_to_room(target_room, force=True):
            self.log.log_gm_action(player, 'Force moved a character')
            for gm in self.player_manager.gamemasters:
                gm.send_gm_character_moved(player, character, source_room, target_room, True)
            target_room.send_character_entered(character, source_room, verbose=False)
            source_room.send_character_left(character, target_room, verbose=False)

    def __eq__(self, other):
        return self.room_manager == other.room_manager and \
               self.char_manager == other.char_manager and \
               self.item_manager == other.item_manager and \
               self.player_manager == other.player_manager
