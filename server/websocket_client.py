from websockets import ConnectionClosed


class WebsocketClient:
    def __init__(self, websocket, game):
        self.socket = websocket
        self.game = game
        self.connected = True

    async def handle(self):
        while self.connected:
            try:
                msg = await self.socket.recv()
            except ConnectionClosed:
                return
            await self.on_message(msg)

    async def on_message(self, msg):
        if msg == 'END':
            await self.send_message('END')
            self.disconnect()

    async def send_message(self, msg):
        await self.socket.send(msg)

    def disconnect(self):
        self.connected = False
