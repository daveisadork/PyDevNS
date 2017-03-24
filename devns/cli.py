import logging
import argparse

from . import config
from .server import DevNS


def main():
    parser = argparse.ArgumentParser(
        prog="devns",
        # formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    log_output_group = parser.add_mutually_exclusive_group()
    log_output_group.add_argument(
        "--verbose", "-v", action="count", dest="verbosity",
        help="verbose output"
    )
    log_output_group.add_argument(
        "--quiet", "-q", action="store_const", const=logging.CRITICAL,
        dest="log_level", help="quiet mode"
    )

    parser.add_argument("--host", type=str, help="address to listen on")
    parser.add_argument("--port", type=int, help="port to listen on")
    parser.add_argument(
        "--address", type=str, help="IP address to respond with"
    )
    resolver_group = parser.add_mutually_exclusive_group()
    resolver_group.add_argument(
        "--no-resolver", "-nr", action="store_false", dest="resolver",
        help="don't put files in /etc/resolver"
    )
    resolver_group.add_argument(
        "domains", type=str, nargs='?',
        help='domains to create resolver files for'
    )

    parser.set_defaults(**config.__dict__)
    parser.parse_args(namespace=config)
    config.log_level = max(10, config.log_level - config.verbosity * 10)
    logging.basicConfig(level=config.log_level)

    app = DevNS()
    return app.run()
