import pytest

from server.websocket_client import WebsocketClient


class TestClientSocket:
    """
    This is a test socket meant for testing the server as a black box.
    """

    def __init__(self, list_in):
        self.list_in = list_in
        self.list_out = []

    async def recv(self):
        """
        Returns messages from a queue of messages to be sent to the server
        """
        if self.list_in:
            return self.list_in.pop(0)
        return 'DISCONNECT'

    async def send(self, message):
        """
        Returns messages that the server sends to the client
        """
        self.list_out.append(message)

    def has_equal_output(self, list_out):
        if self.list_out[-1] == 'DISCONNECT':
            self.list_out = self.list_out[:-1]
        if len(list_out) != len(self.list_out):
            return False
        for i in range(len(list_out)):
            if self.list_out[i] != list_out[i]:
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
