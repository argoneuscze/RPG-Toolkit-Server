class Room:
    def __init__(self, short_name, full_name, description=''):
        self.characters = []
        self.short_name = short_name
        self.full_name = full_name
        self.description = description

    def set_description(self, description):
        ...
