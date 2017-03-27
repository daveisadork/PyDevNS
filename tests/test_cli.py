import pytest
import subprocess

from .fixtures import *  # noqa


@pytest.mark.parametrize("address", ("127.0.0.1", "10.10.10.10"))
def test_parse_args_address(parse_args, config, address):
    parse_args(["--address", address])
    assert config.address == address


@pytest.mark.parametrize(
    "domains, expected",
    [
        ([], ("dev", )),
        (["--domains", "local.dev"], ("local.dev", )),
        (["--domains", "dev", "local.co"], ("dev", "local.co")),
    ]
)
def test_parse_args_domains(parse_args, config, domains, expected):
    parse_args(domains)
    assert config.domains == expected


@pytest.mark.parametrize("host", ("127.0.0.1", "10.10.10.10"))
def test_parse_args_host(parse_args, config, host):
    parse_args(["--host", host])
    assert config.host == host


@pytest.mark.parametrize("args, level", [
    ([], 40),
    (["--quiet"], 50),
    (["-q"], 50)
])
def test_parse_args_quiet(parse_args, config, logger, args, level):
    parse_args(args)
    assert config.log_level == level
    assert logger.getEffectiveLevel() == level


@pytest.mark.parametrize("port", ("0", "53", "53535"))
def test_parse_args_port(parse_args, config, port):
    parse_args(["--port", port])
    assert config.port == int(port)


@pytest.mark.parametrize("args, resolver", [
    ([], True),
    (["--no-resolver"], False),
    (["-nr"], False)
])
def test_parse_args_resolver(parse_args, config, args, resolver):
    parse_args(args)
    assert config.resolver == resolver


@pytest.mark.parametrize("args, resolver_dir", [
    ([], "/etc/resolver"),
    (["--resolver-dir", "/usr/local/etc/resolver"], "/usr/local/etc/resolver"),
])
def test_parse_args_resolver_dir(parse_args, config, args, resolver_dir):
    parse_args(args)
    assert config.resolver_dir == resolver_dir


@pytest.mark.parametrize(
    "args, level", [
        ([], 40),
        (["--verbose"], 30),
        (["-v"], 30),
        (["-vv"], 20),
        (["-vvv"], 10)
    ]
)
def test_parse_args_verbosity(parse_args, config, logger, args, level):
    parse_args(args)
    assert config.log_level == level


def test_executing_as_a_module(parse_args):
    assert subprocess.check_call(("python", "-m", "devns.__main__", "-h")) == 0
