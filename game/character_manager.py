class CharacterManager:
    def __init__(self):
        self.characters = []

    def auth_player(self, player, password):
        for char in self.characters:
            if char.password == password:
                char.add_player(player)
                return True
        return False
