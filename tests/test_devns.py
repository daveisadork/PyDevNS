import os
import sys
import pytest
import socket

from .fixtures import *  # noqa
from devns.server import _intify, DevNS


@pytest.mark.parametrize("value, expected", [
    (1, 1),
    ("1", 49),
    (b"\x01", 1)
])
def test_intify(value, expected):
    assert _intify(value) == expected


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


@pytest.mark.parametrize("host, port", [
    ("0.0.0.0", 53),
    ("0.0.0.0", "0"),
    ("8.8.8.8", 53535),
])
def test_server_bind_error(config, server, host, port):
    config.host = host
    config.port = port
    with server.bind() as connection:
        try:
            assert isinstance(connection, Exception)
        except:
            print(connection.getsockname())
            raise


@pytest.mark.skipif(sys.version_info < (2, 7), reason="Old Python")
@pytest.mark.parametrize("host, port", [
    ("0.0.0.0", -1),
    ("8.8.8.8", 65536)
])
def test_server_bind_error_bad_port(config, server, host, port):
    config.host = host
    config.port = port
    with server.bind() as connection:
        try:
            assert isinstance(connection, Exception)
        except:
            print(connection.getsockname())
            raise


@pytest.mark.parametrize("domains", [("dev", ), ("dev", "local.co")])
def test_server_resolver(config, server, domains, resolver):
    server.config.domains = domains
    with server.bind() as connection:
        _host, _port = connection.getsockname()
        with server._resolver():
            for domain in domains:
                path = os.path.join(resolver, domain)
                assert os.path.isfile(path)

    for domain in domains:
        path = os.path.join(resolver, domain)
        assert not os.path.isfile(path)


@pytest.mark.parametrize("domains", [("dev", ), ("dev", "local.co")])
def test_server_resolver_disabled(config, server, domains, resolver):
    config.domains = domains
    config.resolver = False
    with server.bind() as connection:
        _host, _port = connection.getsockname()
        with server._resolver():
            for domain in domains:
                path = os.path.join(resolver, domain)
                assert not os.path.isfile(path)


@pytest.mark.parametrize("domains", [("dev", "local.co")])
def test_server_resolver_cleanup_error(config, server, domains, resolver):
    server.config.domains = domains
    with server.bind() as connection:
        _host, _port = connection.getsockname()
        with server._resolver():
            for domain in domains:
                path = os.path.join(resolver, domain)
                assert os.path.isfile(path)
            os.unlink(path)

    for domain in domains:
        path = os.path.join(resolver, domain)
        assert not os.path.isfile(path)


def test_server_resolver_error(server):
    with server.bind() as connection:
        _host, _port = connection.getsockname()
        with server._resolver() as resolver:
            assert isinstance(resolver, Exception)

    for domain in server.config.domains:
        path = os.path.join(server.config.resolver_dir, domain)
        assert not os.path.isfile(path)


@pytest.mark.parametrize("address, encoded_address", [
    ("0.0.0.0", b"\x00\x00\x00\x00"),
    ("127.0.0.1", b"\x7f\x00\x00\x01"),
    ("1.2.3.4", b"\x01\x02\x03\x04")
])
def test_server_address(server, address, encoded_address):
    server.address = address
    assert server.address == address
    assert server._encoded_address == encoded_address


@pytest.mark.parametrize("addresses, address", [
    ([], None),
    (["8.8.8.8", "8.8.4.4"], None),
    (["127.0.0.1", "192.168.1.1", "192.168.1.5"], "192.168.1.5"),
    (["8.8.8.8", "8.8.4.4", "127.0.0.1"], "127.0.0.1"),
    (["127.0.0.1", "127.0.1.11", "10.10.10.10"], "10.10.10.10"),
    (["10.10.5.1", "10.10.5.2"], "10.10.5.2"),
    (["10.10.1.1", "192.169.5.5", "127.0.1.12", "172.16.1.5"], "172.16.1.5"),
    (["10.10.3.255", "172.1.1.8", "127.0.1.12", "192.168.1.1"], "192.168.1.1"),
])
def test_server_choose_address(server, addresses, address):
    assert server._choose_address(addresses) == address


@pytest.mark.parametrize("query, expected", [
    (
        b"\x96\xd1\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05local\x03dev\x00\x00\x01\x00\x01",  # noqa
        b"\x96\xd1\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x05local\x03dev\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x01\x02\x03\x04"  # noqa
    ), # noqa
    (
        b"Kj\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x04test\x05local\x03dev\x00\x00\x01\x00\x01",  # noqa
        b"Kj\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00\x04test\x05local\x03dev\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x00<\x00\x04\x01\x02\x03\x04" # noqa
    ),
    (
        b"\x96\xd1\x50\x00\x00\x01\x00\x00\x00\x00\x00\x00\x05local\x03dev\x00\x00\x01\x00\x01", # noqa
        None
    ),
])
def test_build_response(server, query, expected):
    server.address = "1.2.3.4"
    response = server._build_response(query)
    assert response == expected
