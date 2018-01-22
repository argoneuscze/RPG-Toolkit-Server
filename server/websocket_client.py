import asyncio

from server.player_interface import PlayerInterface


class WebsocketClient(PlayerInterface):
    def __init__(self, websocket, game):
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
        if msg == 'DISCONNECT':
            self.disconnect()

    async def send_raw_message(self, msg):
        print('sending ' + msg)
        await self.socket.send(msg)

    def disconnect(self):
        self.schedule_raw_message('DISCONNECT')
        self.connected = False

    def schedule_raw_message(self, msg):
        self.send_queue.put_nowait(msg)
