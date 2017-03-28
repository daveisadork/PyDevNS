import os
import pytest
import logging
import functools

import devns

from mock import MagicMock


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
    config.resolver_dir = os.path.abspath("./_resolver")
    return devns.server.DevNS(config)


@pytest.yield_fixture
def resolver(config, server):
    resolver = os.path.abspath("./resolver")
    if not os.path.isdir(resolver):
        os.mkdir(resolver)
    config.resolver_dir = resolver
    yield resolver
    os.rmdir(resolver)


class Connection(object):
    def __init__(self, responses, expected):
        self.responses = responses
        self.expected = expected

    settimeout = MagicMock()
    bind = MagicMock()
    sendto = MagicMock()

    def getsockname(self):
        return "0.0.0.0", 53535

    def recvfrom(self, length):
        response = self.responses.pop()
        if isinstance(response, tuple):
            return response
        raise response()
