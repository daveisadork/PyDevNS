import pytest

from .fixtures import *  # noqa
from six import iteritems


def test_config_defaults(config):
    for key, value in iteritems(config.DEFAULTS):
        assert getattr(config, key) == value


@pytest.mark.parametrize("address", ("127.0.0.1", "10.10.10.10"))
def test_config_address(config, address):
    config.address = address
    assert config.address == address


@pytest.mark.parametrize(
    "domains, expected",
    [
        (["local.dev"], ("local.dev", )),
        (["local.dev", "local.co"], ("local.dev", "local.co")),
        (("local.dev", "local.co"), ("local.dev", "local.co")),
        ("local.dev", ("local.dev", )),
    ]
)
def test_config_domains(config, domains, expected):
    config.domains = domains
    assert config.domains == expected


@pytest.mark.parametrize("host", ("127.0.0.1", "10.10.10.10"))
def test_config_host(config, host):
    config.host = host
    assert config.host == host


@pytest.mark.parametrize("level", range(10, 60, 10))
def test_config_log_level(logger, config, level):
    config.log_level = level
    assert config.log_level == level
    assert logger.getEffectiveLevel() == level


@pytest.mark.parametrize("port", (0, 53, 53535))
def test_config_port(config, port):
    config.port = port
    assert config.port == port


@pytest.mark.parametrize("resolver", (True, False))
def test_config_resolver(config, resolver):
    config.resolver = resolver
    assert config.resolver == resolver


@pytest.mark.parametrize("resolver_dir", [
    "/usr/local/etc/resolver",
    "~/.config/resolver",
])
def test_parse_args_resolver_dir(config, resolver_dir):
    config.resolver_dir = resolver_dir
    assert config.resolver_dir == resolver_dir


@pytest.mark.parametrize(
    "verbosity, level", [(0, 40), (1, 30), (2, 20), (3, 10)]
)
def test_config_verbosity(logger, config, verbosity, level):
    config.verbosity = verbosity
    assert config.log_level == level
    assert config.verbosity == verbosity
