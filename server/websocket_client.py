import asyncio

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
        cmd, arg_list = self.parse_command(msg)
        try:
            self.dispatch[cmd](self, arg_list)
        except KeyError:
            # invalid command
            return
        except ValueError:
            # invalid arguments
            return

    async def send_raw_message(self, msg):
        print('sending ' + msg)
        await self.socket.send(msg)

    def disconnect(self):
        self.schedule_raw_message('DISCONNECT')
        self.connected = False

    def schedule_raw_message(self, msg):
        self.send_queue.put_nowait(msg)

    def parse_command(self, msg):
        spl = msg.split(maxsplit=1)
        if len(spl) == 1:
            return spl[0], ''
        return spl[0], spl[1]

    def validate_args(self, arg_list_orig, *types_orig):
        arg_list_str = arg_list_orig
        types = types_orig[:]
        ret_vals = []
        for i in range(len(types)):
            type_name = types[i]
            if not arg_list_str:
                raise ValueError('Too few arguments')
            if type_name == 'long_str':
                ret_vals.append(arg_list_str)
                arg_list_str = ''
            else:
                spl = arg_list_str.split(maxsplit=1)
                val = spl.pop(0)
                if type_name == 'int':
                    ret_vals.append(int(val))
                elif type_name == 'str':
                    ret_vals.append(val)
                arg_list_str = ''
                if spl:
                    arg_list_str = spl[0]
        if arg_list_str:
            raise ValueError('Too many arguments')
        if len(ret_vals) == 1:
            return ret_vals[0]
        return ret_vals

    def cmd_disconnect(self, arg_list):
        self.validate_args(arg_list)
        self.disconnect()

    def cmd_ident_player(self, arg_list):
        password = self.validate_args(arg_list, 'long_str')
        # TODO

    def cmd_ident_gm(self, arg_list):
        password = self.validate_args(arg_list, 'long_str')
        # TODO

    dispatch = {
        'DISCONNECT': cmd_disconnect,
        'IDENTPLAYER': cmd_ident_player,
        'IDENTGM': cmd_ident_gm
    }
