import asyncio
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
        self.delay = 0

    async def recv(self):
        """
        Returns messages from a queue of messages to be sent to the server
        """
        if self.data_in:
            return json.dumps(self.data_in.pop(0))
        if self.delay > 0:
            await asyncio.sleep(self.delay)  # grace period to wait for further messages
        return json.dumps(TestClientSocket.DISC_CMD)

    async def send(self, message):
        """
        Returns messages that the server sends to the client
        """
        self.data_out.append(json.loads(message))

    def has_equal_output(self, data_out):
        if self.data_out[-1] == TestClientSocket.DISC_CMD:
            self.data_out = self.data_out[:-1]
        print('Expected: {}'.format(data_out))
        print('Received: {}'.format(self.data_out))
        if len(data_out) != len(self.data_out):
            return False
        for i in range(len(data_out)):
            if self.data_out[i] != data_out[i]:
                return False
        return True

    def set_wait_delay(self, delay):
        self.delay = delay


@pytest.fixture
def socket():
    def construct_socket(data_in):
        return TestClientSocket(data_in)

    return construct_socket


@pytest.fixture
def new_client(basic_game, socket):
    def construct_client(data_in):
        return WebsocketClient(socket(data_in), basic_game)

    return construct_client


@pytest.fixture
def player_client(basic_game, socket):
    def construct_player(character, ooc_name, data_in):
        client = WebsocketClient(socket(data_in), basic_game)
        basic_game.player_manager.auth_client_player(client, character.password, ooc_name)
        return client

    return construct_player


@pytest.fixture
def gm_client(basic_game, socket, gm_password):
    def construct_gm(ooc_name, data_in):
        client = WebsocketClient(socket(data_in), basic_game)
        basic_game.player_manager.auth_client_gm(client, gm_password, ooc_name)
        return client

    return construct_gm


def room_to_json(room):
    expected_characters = []

    for char in room.characters:
        expected_characters.append({
            'short_name': char.short_name,
            'full_name': char.full_name
        })

    room_data = {
        'command': 'roominfo',
        'room_short_name': room.short_name,
        'room_long_name': room.long_name,
        'room_description': room.description,
        'adjacent_rooms': [{'short_name': room.short_name, 'long_name': room.long_name}
                           for room in room.adjacent_rooms],
        'characters': expected_characters
    }

    return room_data
