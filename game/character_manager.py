class CharacterManager:
    def __init__(self):
        self.characters = []

    def get_char_by_password(self, password):
        for char in self.characters:
            if char.password == password:
                return char
        return None
