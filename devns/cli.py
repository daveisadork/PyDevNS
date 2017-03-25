import logging
import argparse

from . import config
from .server import DevNS


def parse_args(args=None, config=config):
    parser = argparse.ArgumentParser(prog="devns")
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
        "--domains", type=str, nargs="*", metavar="DOMAIN",
        help='domains to create resolver files for'
    )

    parser.set_defaults(**config.DEFAULTS)
    return parser.parse_args(args, namespace=config)


def main():  # pragma no cover
    app = DevNS(parse_args())
    return app.run()
