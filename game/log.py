class GameLog:
    def __init__(self):
        self.file = None

    def open_file(self, directory, filename):
        self.file = open("{}/{}".format(directory, filename), "a")

    def write_message(self, msg):
        if self.file is not None:
            self.file.write("{}\n".format(msg))
            self.file.flush()

    def log_player_action(self, player, message):
        self.write_message('[ACTION][{}] {}'.format(player.ooc_name, message))

    def log_gm_action(self, player, message):
        self.write_message('[ GM] {}: {}'.format(player.ooc_name, message))

    def log_message_ic(self, character, message):
        room = character.room
        name = character.full_name
        self.write_message('[ IC][{}] {}: {}'.format(room.long_name, name, message))

    def log_message_ooc(self, character, player, message):
        room = character.room
        name = player.ooc_name
        self.write_message('[OOC][{}] {}: {}'.format(room.long_name, name, message))
