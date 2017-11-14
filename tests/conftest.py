import functools
import logging
import os
import pytest
import tempfile

import devns
import devns.cli

from mock import MagicMock


@pytest.fixture
def config():
    return devns.Config()


@pytest.yield_fixture
def resolver_dir(config):
    resolvers = []
    config.resolver_dir = os.path.join(
        tempfile.gettempdir(),
        "{0}-{1}".format(tempfile.gettempprefix(), "resolver")
    )
    resolvers.append(config.resolver_dir)
    yield config.resolver_dir
    resolvers.append(config.resolver_dir)
    for resolver in filter(None, set(resolvers)):
        if os.path.isdir(resolver):
            os.rmdir(resolver)


@pytest.fixture
def logger(request):
    return logging.getLogger(request.node.nodeid)


@pytest.fixture
def parse_args(config):
    return functools.partial(devns.cli.parse_args, config=config)


@pytest.yield_fixture
def server(config, resolver_dir):
    yield devns.server.DevNS(config)


@pytest.fixture
def Connection():
    class Connection(object):
        settimeout = MagicMock()
        bind = MagicMock()
        sendto = MagicMock()

        def __init__(self, responses, expected):
            self.responses = responses
            self.expected = expected

        def getsockname(self):
            return "0.0.0.0", 53535

        def recvfrom(self, length):
            response = self.responses.pop()
            if isinstance(response, tuple):
                return response
            raise response()

    return Connection
