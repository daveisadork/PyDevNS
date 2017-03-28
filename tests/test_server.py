import os
import sys
import pytest
import socket

from .fixtures import *  # noqa
from datetime import timedelta
from mock import patch, MagicMock
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
        assert isinstance(connection, Exception)


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


@pytest.mark.parametrize("address, encoded_address", [
    ("0.0.0.0", b"\x00\x00\x00\x00"),
    ("127.0.0.1", b"\x7f\x00\x00\x01"),
    ("1.2.3.4", b"\x01\x02\x03\x04")
])
def test_server_address_ttl(server, address, encoded_address):
    server.address = "1.2.3.4"
    server._address_last_updated -= timedelta(seconds=server.config.ttl + 5)
    last_updated = server._address_last_updated
    with patch("devns.server.DevNS._get_address_by_ifconfig") as ifconfig:
        ifconfig.return_value = address
        assert server.address == address
        assert server._encoded_address == encoded_address
        assert server._address_last_updated > last_updated
        ifconfig.assert_called_once()


@pytest.mark.parametrize("address, encoded_address", [
    ("0.0.0.0", b"\x00\x00\x00\x00"),
    ("127.0.0.1", b"\x7f\x00\x00\x01"),
    ("1.2.3.4", b"\x01\x02\x03\x04")
])
def test_server_ttl_config_address(server, address, encoded_address):
    server.config.address = address
    with patch("devns.server.DevNS._get_address_by_ifconfig") as ifconfig:
        assert server.address == address
        assert server._encoded_address == encoded_address
        assert server._address_age == 0
        ifconfig.assert_not_called()


def test_server_get_address_by_hostname(server):
    with patch("devns.server.socket") as socket_mock:
        socket_mock.getfqdn = MagicMock(return_value="test.example.com")
        socket_mock.gethostbyname = MagicMock(return_value="10.10.10.10")
        address = server._get_address_by_hostname()
        socket_mock.getfqdn.assert_called_once_with()
        socket_mock.gethostbyname.assert_called_once_with("test.example.com")
    assert address == "10.10.10.10"


def test_server_get_address_by_hostname_error(server):
    with patch("devns.server.socket") as socket_mock:
        socket_mock.getfqdn = MagicMock(return_value="test.example.com")
        socket_mock.gethostbyname = MagicMock(side_effect=socket.error)
        address = server._get_address_by_hostname()
        socket_mock.getfqdn.assert_called_once_with()
        socket_mock.gethostbyname.assert_called_once_with("test.example.com")

    assert address is None


def test_server_address_error(server):
    with patch("devns.server.subprocess") as subprocess:
        with patch("devns.server.socket") as socket_mock:
            socket_mock.getfqdn = MagicMock(return_value="test.example.com")
            socket_mock.gethostbyname = MagicMock(side_effect=socket.error)
            subprocess.check_output = MagicMock(return_value="")
            with pytest.raises(RuntimeError):
                server.address = None
            socket_mock.getfqdn.assert_called_once_with()
            socket_mock.gethostbyname.assert_called_once_with(
                "test.example.com"
            )
            subprocess.check_output.assert_called_once_with(("ifconfig", ))


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
def test_server_build_response(server, query, expected):
    config.address = server.address = "1.2.3.4"
    response = server._build_response(query)
    assert response == expected


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
def test_server_listen(config, server, query, expected):
    config.address = server.address = "1.2.3.4"

    server.connection = Connection([
        KeyboardInterrupt,
        (query, ("127.0.0.1", 5000)),
        socket.error,
        (query, ("127.0.0.1", 5000)),
        socket.error
    ], expected)

    assert pytest.raises(KeyboardInterrupt, server._listen)


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
def test_server_run(config, server, query, expected):
    config.resolver = False
    config.address = server.address = "1.2.3.4"
    connection = Connection([
        KeyboardInterrupt,
        (query, ("127.0.0.1", 5000)),
        socket.error
    ], expected)

    with patch("devns.server.socket.socket") as socket_mock:
        socket_mock.return_value = connection
        assert server.run() == 0


def test_server_run_bind_failure(config, server):
    config.port = ""
    assert server.run() == 2


def test_server_run_resolver_failure(server, resolver):
    os.chmod(resolver, 400)
    assert server.run() == 3
    os.chmod(resolver, 777)


@pytest.mark.parametrize("ifconfig, expected", [
    ("\n".join([
        "lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384",
        "        options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>",
        "        inet 127.0.0.1 netmask 0xff000000",
        "        inet6 ::1 prefixlen 128",
        "        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1",
        "        nd6 options=201<PERFORMNUD,DAD>",
        "gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280",
        "stf0: flags=0<> mtu 1280",
        "en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500",  # noqa
        "        ether a4:5e:60:ee:b9:55",
        "        inet 10.10.10.10 netmask 0xffffff00 broadcast 10.10.10.255",
        "        nd6 options=201<PERFORMNUD,DAD>",
        "        media: autoselect",
        "        status: active"
    ]), "10.10.10.10"),
    (b"\n".join([
        b"lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384",
        b"        options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>",
        b"        inet 127.0.0.1 netmask 0xff000000",
        b"        inet6 ::1 prefixlen 128",
        b"        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1",
        b"        nd6 options=201<PERFORMNUD,DAD>",
        b"gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280",
        b"stf0: flags=0<> mtu 1280",
        b"en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500",  # noqa
        b"        ether a4:5e:60:ee:b9:55",
        b"        inet 10.10.10.10 netmask 0xffffff00 broadcast 10.10.10.255",
        b"        nd6 options=201<PERFORMNUD,DAD>",
        b"        media: autoselect",
        b"        status: active"
    ]), "10.10.10.10"),
    ("\n".join([
        "br-27494a0950d6 Link encap:Ethernet  HWaddr 02:42:7f:e2:16:f6",
        "          inet addr:172.19.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        "          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        "          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        "          collisions:0 txqueuelen:0",
        "          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        "",
        "br-279eacf22928 Link encap:Ethernet  HWaddr 02:42:d2:4f:90:98",
        "          inet addr:172.20.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        "          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        "          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        "          collisions:0 txqueuelen:0",
        "          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        "",
        "br-6ce4900259e9 Link encap:Ethernet  HWaddr 02:42:7d:d4:e4:a3",
        "          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        "          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        "          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        "          collisions:0 txqueuelen:0",
        "          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        "",
        "docker0   Link encap:Ethernet  HWaddr 02:42:31:08:c9:7a",
        "          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        "          inet6 addr: fe80::42:31ff:fe08:c97a/64 Scope:Link",
        "          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
        "          RX packets:476239594 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:692721303 errors:0 dropped:0 overruns:0 carrier:0",  # noqa
        "          collisions:0 txqueuelen:0",
        "          RX bytes:40052256393 (40.0 GB)  TX bytes:1937960295820 (1.9 TB)",  # noqa
        "",
        "em1       Link encap:Ethernet  HWaddr d8:d3:85:5e:37:e6",
        "          inet addr:10.10.10.49  Bcast:10.10.10.255  Mask:255.255.255.0",  # noqa
        "          inet6 addr: fe80::dad3:85ff:fe5e:37e6/64 Scope:Link",
        "          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
        "          RX packets:2061109619 errors:2 dropped:0 overruns:2 frame:1",
        "          TX packets:2093831600 errors:0 dropped:0 overruns:0 carrier:0",  # noqa
        "          collisions:0 txqueuelen:1000",
        "          RX bytes:2386493461462 (2.3 TB)  TX bytes:2245604822541 (2.2 TB)",  # noqa
        "          Memory:c0400000-c041ffff",
        "",
        "lo        Link encap:Local Loopback",
        "          inet addr:127.0.0.1  Mask:255.0.0.0",
        "          inet6 addr: ::1/128 Scope:Host",
        "          UP LOOPBACK RUNNING  MTU:65536  Metric:1",
        "          RX packets:150372537 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:150372537 errors:0 dropped:0 overruns:0 carrier:0",  # noqa
        "          collisions:0 txqueuelen:1",
        "          RX bytes:91406483840 (91.4 GB)  TX bytes:91406483840 (91.4 GB)",  # noqa
        "",
        "lxcbr0    Link encap:Ethernet  HWaddr 00:16:3e:00:00:00",
        "          inet addr:10.0.3.1  Bcast:0.0.0.0  Mask:255.255.255.0",
        "          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        "          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        "          collisions:0 txqueuelen:1000",
        "          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        "",
        "veth5819543 Link encap:Ethernet  HWaddr 96:66:95:e3:b2:24",
        "          inet6 addr: fe80::9466:95ff:fee3:b224/64 Scope:Link",
        "          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
        "          RX packets:398508 errors:0 dropped:0 overruns:0 frame:0",
        "          TX packets:2606383 errors:0 dropped:0 overruns:0 carrier:0",
        "          collisions:0 txqueuelen:0",
        "          RX bytes:22700793 (22.7 MB)  TX bytes:299182613 (299.1 MB)",
        ""
    ]), "10.10.10.49"),
    (b"\n".join([
        b"br-27494a0950d6 Link encap:Ethernet  HWaddr 02:42:7f:e2:16:f6",
        b"          inet addr:172.19.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        b"          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        b"          collisions:0 txqueuelen:0",
        b"          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        b"",
        b"br-279eacf22928 Link encap:Ethernet  HWaddr 02:42:d2:4f:90:98",
        b"          inet addr:172.20.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        b"          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        b"          collisions:0 txqueuelen:0",
        b"          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        b"",
        b"br-6ce4900259e9 Link encap:Ethernet  HWaddr 02:42:7d:d4:e4:a3",
        b"          inet addr:172.18.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        b"          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        b"          collisions:0 txqueuelen:0",
        b"          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        b"",
        b"docker0   Link encap:Ethernet  HWaddr 02:42:31:08:c9:7a",
        b"          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0",
        b"          inet6 addr: fe80::42:31ff:fe08:c97a/64 Scope:Link",
        b"          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:476239594 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:692721303 errors:0 dropped:0 overruns:0 carrier:0",  # noqa
        b"          collisions:0 txqueuelen:0",
        b"          RX bytes:40052256393 (40.0 GB)  TX bytes:1937960295820 (1.9 TB)",  # noqa
        b"",
        b"em1       Link encap:Ethernet  HWaddr d8:d3:85:5e:37:e6",
        b"          inet addr:10.10.10.49  Bcast:10.10.10.255  Mask:255.255.255.0",  # noqa
        b"          inet6 addr: fe80::dad3:85ff:fe5e:37e6/64 Scope:Link",
        b"          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:2061109619 errors:2 dropped:0 overruns:2 frame:1",  # noqa
        b"          TX packets:2093831600 errors:0 dropped:0 overruns:0 carrier:0",  # noqa
        b"          collisions:0 txqueuelen:1000",
        b"          RX bytes:2386493461462 (2.3 TB)  TX bytes:2245604822541 (2.2 TB)",  # noqa
        b"          Memory:c0400000-c041ffff",
        b"",
        b"lo        Link encap:Local Loopback",
        b"          inet addr:127.0.0.1  Mask:255.0.0.0",
        b"          inet6 addr: ::1/128 Scope:Host",
        b"          UP LOOPBACK RUNNING  MTU:65536  Metric:1",
        b"          RX packets:150372537 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:150372537 errors:0 dropped:0 overruns:0 carrier:0",  # noqa
        b"          collisions:0 txqueuelen:1",
        b"          RX bytes:91406483840 (91.4 GB)  TX bytes:91406483840 (91.4 GB)",  # noqa
        b"",
        b"lxcbr0    Link encap:Ethernet  HWaddr 00:16:3e:00:00:00",
        b"          inet addr:10.0.3.1  Bcast:0.0.0.0  Mask:255.255.255.0",
        b"          UP BROADCAST MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:0 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0",
        b"          collisions:0 txqueuelen:1000",
        b"          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)",
        b"",
        b"veth5819543 Link encap:Ethernet  HWaddr 96:66:95:e3:b2:24",
        b"          inet6 addr: fe80::9466:95ff:fee3:b224/64 Scope:Link",
        b"          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1",
        b"          RX packets:398508 errors:0 dropped:0 overruns:0 frame:0",
        b"          TX packets:2606383 errors:0 dropped:0 overruns:0 carrier:0",
        b"          collisions:0 txqueuelen:0",
        b"          RX bytes:22700793 (22.7 MB)  TX bytes:299182613 (299.1 MB)",
        b""
    ]), "10.10.10.49"),
])
def test_server_get_address_by_ifconfig(server, ifconfig, expected):
    with patch("devns.server.subprocess") as subprocess:
        subprocess.check_output = MagicMock(return_value=ifconfig)
        address = server._get_address_by_ifconfig()
        subprocess.check_output.assert_called_once_with(("ifconfig", ))
    assert address == expected
