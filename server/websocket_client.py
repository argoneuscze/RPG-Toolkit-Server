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
        print('received ' + msg)
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

    async def send_raw_message(self, msg):
        print('sending ' + msg)
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

    def cmd_disconnect(self, _):
        self.disconnect()

    def cmd_ident_player(self, data):
        password = data['password']
        ooc_name = data['ooc_name']
        self.game.new_player_character(self, password, ooc_name)

    def cmd_ident_gm(self, data):
        password = data['password']
        ooc_name = data['ooc_name']
        self.game.new_player_gm(self, password, ooc_name)

    dispatch = {
        'disconnect': cmd_disconnect,
        'identplayer': cmd_ident_player,
        'identgm': cmd_ident_gm
    }
