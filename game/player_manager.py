import json

from game.player import Player


class PlayerManager:
    """Manager responsible for authorizing new Players trying to connect to the Game."""

    def __init__(self, char_manager):
        self.clients = dict()
        self.char_players = dict()
        self.gamemasters = set()
        self.char_manager = char_manager
        self.gm_passwords = set()

    def auth_client_player(self, client, password, ooc_name):
        """Attempts to authorize a new client as a player character given a character password."""

        char = self.char_manager.get_char_by_password(password)
        if not char:
            return None, None
        p = Player(client, ooc_name, False)
        char.add_player(p)
        self.char_players[p] = char
        self.clients[client] = p
        return p, char

    def auth_client_gm(self, client, password, ooc_name):
        """Attempts to authorize a new client as a gamemaster given a GM password."""

        if password not in self.gm_passwords:
            return None
        p = Player(client, ooc_name, True)
        self.gamemasters.add(p)
        self.clients[client] = p
        return p

    def remove_player(self, client):
        """Removes the player from the game entirely."""

        p = self.clients.get(client)
        if p is None:
            return
        del self.clients[client]
        if p.is_gm:
            self.gamemasters.remove(p)
        else:
            self.char_players[p].remove_player(p)
            del self.char_players[p]

    def load_gm_passwords(self, gamedir):
        data = json.load(open("{}/gm_passwords.json".format(gamedir)))
        self.gm_passwords = set(data['passwords'])

    def get_player(self, client):
        player = self.clients.get(client)
        if player.is_gm:
            return player, None
        return player, self.char_players[player]

    def get_gm(self, client):
        player = self.clients.get(client)
        if player.is_gm:
            return player
        return None

    def __eq__(self, other):
        return self.gm_passwords == other.gm_passwords
