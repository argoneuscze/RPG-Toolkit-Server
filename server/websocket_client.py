import asyncio
import json
from json import JSONDecodeError

from server.player_interface import PlayerInterface


class WebsocketClient(PlayerInterface):
    def __init__(self, websocket, game):
        self.dispatch = self.__class__.dispatch
        self.socket = websocket
        self.game = game
        self.send_queue = asyncio.Queue()
        self.connected = True

    async def handle(self):
        recv_task = asyncio.ensure_future(self.socket.recv())
        queue_task = asyncio.ensure_future(self.send_queue.get())
        pending = {recv_task, queue_task}

        while self.connected:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                if task.exception() is not None:
                    self.disconnect()
                    return

                if task is recv_task:
                    msg = task.result()
                    await self.on_message(msg)
                    recv_task = asyncio.ensure_future(self.socket.recv())
                    pending.add(recv_task)
                elif task is queue_task:
                    msg = task.result()
                    await self.send_raw_message(msg)
                    queue_task = asyncio.ensure_future(self.send_queue.get())
                    pending.add(queue_task)

        recv_task.cancel()
        queue_task.cancel()

        # send the rest of the queue
        for _ in range(self.send_queue.qsize()):
            await self.send_raw_message(self.send_queue.get_nowait())

    async def on_message(self, msg):
        try:
            cmd, data = self.parse_command(msg)
            self.dispatch[cmd](self, data)
        except JSONDecodeError:
            # invalid json
            return
        except KeyError:
            # invalid command or arguments
            return
        except ValueError:
            # invalid argument types
            return
        except PermissionError:
            # don't have permissions for said command
            return

    async def send_raw_message(self, msg):
        await self.socket.send(msg)

    def schedule_raw_message(self, msg):
        self.send_queue.put_nowait(msg)

    def schedule_command(self, command, args_dict=None):
        data = {'command': command}
        if args_dict is not None:
            data.update(args_dict)
        self.schedule_raw_message(json.dumps(data))

    def parse_command(self, msg):
        data = json.loads(msg)
        cmd = data['command']
        return cmd, data

    def disconnect(self):
        self.schedule_command('disconnect')
        self.connected = False
        self.game.remove_client(self)

    def cmd_disconnect(self, _):
        self.disconnect()

    def cmd_identplayer(self, data):
        password = data['password']
        ooc_name = data['ooc_name']
        self.game.new_player_character(self, password, ooc_name)

    def cmd_identgm(self, data):
        password = data['password']
        ooc_name = data['ooc_name']
        self.game.new_player_gm(self, password, ooc_name)

    def cmd_messageic(self, data):
        message = data['message']
        self.game.message_ic(self, message)

    def cmd_messageooc(self, data):
        message = data['message']
        self.game.message_ooc(self, message)

    def cmd_playermove(self, data):
        room = data['target_room']
        self.game.move_player(self, room)

    def cmd_gmforcemove(self, data):
        character = data['character']
        target_room = data['target_room']
        self.game.gm_move_character(self, character, target_room)

    dispatch = {
        'disconnect': cmd_disconnect,
        'identplayer': cmd_identplayer,
        'identgm': cmd_identgm,
        'messageic': cmd_messageic,
        'messageooc': cmd_messageooc,
        'playermove': cmd_playermove,

        'gmforcemove': cmd_gmforcemove
    }

    def send_auth_ok(self):
        self.schedule_command('auth_ok')

    def send_auth_failure(self, message):
        self.schedule_command('auth_failure', {'message': message})

    def send_room_info(self, room):
        chars = []
        for char in room.characters:
            chars.append({
                'short_name': char.short_name,
                'full_name': char.full_name
            })
        data = {
            'room_short_name': room.short_name,
            'room_long_name': room.long_name,
            'room_description': room.description,
            'adjacent_rooms': [{'short_name': room.short_name, 'long_name': room.long_name}
                               for room in room.adjacent_rooms],
            'characters': chars
        }
        self.schedule_command('roominfo', data)

    def send_message_ic(self, char_from, message):
        data = {
            'character_short_name': char_from.short_name,
            'character_full_name': char_from.full_name,
            'message': message
        }
        self.schedule_command('messageic', data)

    def send_message_ooc(self, player_from, message):
        data = {
            'player_name': player_from.ooc_name,
            'message': message
        }
        self.schedule_command('messageooc', data)

    def send_character_left_room(self, character, room, verbose):
        data = {
            'char_short_name': character.short_name,
            'char_full_name': character.full_name,
            'room_to_short_name': room.short_name,
            'room_to_long_name': room.short_name,
            'verbose': verbose
        }
        self.schedule_command('charleave', data)

    def send_character_entered_room(self, character, room, verbose):
        data = {
            'char_short_name': character.short_name,
            'char_full_name': character.full_name,
            'room_from_short_name': room.short_name,
            'room_from_long_name': room.short_name,
            'verbose': verbose
        }
        self.schedule_command('charenter', data)

    def send_gm_character_moved(self, player, character, source_room, target_room, force):
        data = {
            'gm_ooc_name': player.ooc_name,
            'character': character.short_name,
            'source_room': source_room.short_name,
            'target_room': target_room.short_name,
            'was_forced': force
        }
        self.schedule_command('gmcharmove', data)
