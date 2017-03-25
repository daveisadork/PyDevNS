import pytest
import logging
import functools

import devns


@pytest.fixture
def config():
    return devns.Config()


@pytest.fixture
def logger(request):
    return logging.getLogger(request.node.nodeid)


@pytest.fixture
def parse_args(config):
    return functools.partial(devns.cli.parse_args, config=config)


@pytest.fixture
def server(config):
    return devns.server.DevNS(config)
