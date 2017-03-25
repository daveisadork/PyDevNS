import pytest
import socket

from .fixtures import *  # noqa
from devns.server import DevNS


def test_server_init_no_config(config):
    server = DevNS()
    assert server.config._data == config._data
    assert server.config is not config


def test_server_init_with_config(config):
    server = DevNS(config)
    assert server.config is config


def test_server_init_with_kwargs(config):
    DevNS(config, host="127.0.0.1", port=53, address="10.10.10.10")
    assert config.port == 53
    assert config.host == "127.0.0.1"
    assert config.address == "10.10.10.10"


@pytest.mark.parametrize("host, port", [
    ("0.0.0.0", 0),
    ("127.0.0.1", 53535)
])
def test_server_bind(config, server, host, port):
    config.host = host
    config.port = port
    with server.bind() as connection:
        assert server.connection is connection
        timeout = connection.gettimeout()
        _host, _port = connection.getsockname()

    assert timeout == 3.05
    assert _host == host
    assert _port == port or _port
    with pytest.raises(socket.error):
        server.connection.getsockname()
