import json

import pytest

from server.websocket_client import WebsocketClient


class TestClientSocket:
    """
    This is a test socket meant for testing the server as a black box.
    """

    DISC_CMD = {'command': 'disconnect'}

    def __init__(self, data_in):
        self.data_in = data_in
        self.data_out = []

    async def recv(self):
        """
        Returns messages from a queue of messages to be sent to the server
        """
        if self.data_in:
            return json.dumps(self.data_in.pop(0))
        return json.dumps(TestClientSocket.DISC_CMD)

    async def send(self, message):
        """
        Returns messages that the server sends to the client
        """
        self.data_out.append(json.loads(message))

    def has_equal_output(self, data_out):
        if self.data_out[-1] == TestClientSocket.DISC_CMD:
            self.data_out = self.data_out[:-1]
        if len(data_out) != len(self.data_out):
            return False
        for i in range(len(data_out)):
            if self.data_out[i] != data_out[i]:
                return False
        return True


@pytest.fixture
def socket():
    def construct_socket(list_in):
        return TestClientSocket(list_in)

    return construct_socket


@pytest.fixture
def player_client(game):
    def construct_player(sock):
        return WebsocketClient(sock, game)

    return construct_player
