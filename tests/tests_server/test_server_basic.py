import pytest


@pytest.mark.asyncio
async def test_server_connection(player_client):
    data_in = []
    data_out = []

    client = player_client(data_in)
    await client.handle()

    assert client.socket.has_equal_output(data_out)
