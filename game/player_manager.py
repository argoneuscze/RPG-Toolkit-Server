import json

from game.player import Player


class PlayerManager:
    def __init__(self, char_manager):
        self.clients = dict()
        self.char_players = dict()
        self.gamemasters = set()
        self.char_manager = char_manager
        self.gm_passwords = set()

        self.load_gm_passwords()

    def auth_client_player(self, ooc_name, client, password):
        char = self.char_manager.get_char_by_password(password)
        if not char:
            return None
        p = Player(ooc_name, client, False)
        char.add_player(p)
        self.char_players[p] = char
        self.clients[client] = p
        return p

    def auth_client_gm(self, ooc_name, client, password):
        if password not in self.gm_passwords:
            return None
        p = Player(ooc_name, client, True)
        self.gamemasters.add(p)
        self.clients[client] = p
        return p

    def remove_player(self, client):
        p = self.clients[client]
        del self.clients[client]
        if p.is_gm:
            self.gamemasters.remove(p)
        else:
            self.char_players[p].remove_player(p)
            del self.char_players[p]

    def load_gm_passwords(self):
        data = json.load(open("config/gm_passwords.json"))
        self.gm_passwords = set(data['passwords'])
