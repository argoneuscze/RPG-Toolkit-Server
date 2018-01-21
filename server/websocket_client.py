class WebsocketClient:
    def __init__(self, websocket, game):
        self.socket = websocket

    async def handle(self):
        while True:
            msg = self.socket.recv()
            await self.on_message(msg)

    async def on_message(self, msg):
        print(msg)
