import pytest


@pytest.mark.asyncio
async def test_server_connection(new_client):
    data_in = []
    data_out = []

    client = new_client(data_in)
    await client.handle()

    assert client.socket.has_equal_output(data_out)
