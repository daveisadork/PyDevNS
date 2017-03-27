import os
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


@pytest.fixture
def resolver(config, server):
    resolver = os.path.abspath("./resolver")
    if not os.path.isdir(resolver):
        os.mkdir(resolver)
    config.resolver_dir = resolver
    yield resolver
    for item in os.listdir(resolver):
        os.unlink(os.path.join(resolver, item))
    os.rmdir(resolver)
