import pytest


@pytest.mark.asyncio
async def test_server_connection(player_client, socket):
    data_in = []
    data_out = []

    socket_1 = socket(data_in)
    client = player_client(socket_1)

    await client.handle()

    assert socket_1.has_equal_output(data_out)
