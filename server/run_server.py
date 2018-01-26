import asyncio
import sys

import websockets

from game.game import Game
from server.websocket_client import WebsocketClient


class Server:
    def __init__(self, game):
        self.game = game

    async def handler(self, websocket, _path):
        client = WebsocketClient(websocket, self.game)
        await client.handle()

    def run(self):
        server_cr = websockets.serve(self.handler, 'localhost', 7777)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(server_cr)
        loop.run_forever()


def start_server():
    g = Game()
    g.load_game(sys.argv[1])
    s = Server(g)
    s.run()


if __name__ == '__main__':
    start_server()
