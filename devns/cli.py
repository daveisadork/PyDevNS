import sys
import logging
import argparse

from .server import DevNS
from . import config, __version__


def parse_args(args=None, config=config):
    parser = argparse.ArgumentParser(
        description="PyDevNS - A DNS server for developers."
    )
    parser.add_argument(
        '--version',
        action='version',
        version=__version__,
        help="show version and exit"
    )
    log_group = parser.add_argument_group("Logging")
    log_output_group = log_group.add_mutually_exclusive_group()
    log_output_group.add_argument(
        "--verbose", "-v", action="count", dest="verbosity",
        help="verbose output"
    )
    log_output_group.add_argument(
        "--quiet", "-q", action="store_const", const=logging.CRITICAL,
        dest="log_level", help="quiet mode"
    )

    address = parser.add_argument_group("Address")
    address_group = address.add_mutually_exclusive_group()
    address_group.add_argument(
        "--address", "-a", type=str, help="IP address to respond with"
    )
    address_group.add_argument(
        "--ttl", "-t", type=int, metavar="SECONDS",
        help="how often to refresh the address"
    )

    listen = parser.add_argument_group("Network")
    listen.add_argument("--host", "-H", type=str, help="address to listen on")
    listen.add_argument("--port", "-p", type=int, help="port to listen on")

    resolver_group = parser.add_argument_group("Resolver")
    resolver_group.add_argument(
        "--domains", "-d", type=str, nargs="*", metavar="DOMAIN",
        help="domains to create resolver files for"
    )
    resolver_group.add_argument(
        "--resolver-dir", "-rd", type=str, metavar="DIRECTORY",
        dest="resolver_dir", help="where to put resolver files"
    )
    resolver_group.add_argument(
        "--no-resolver", "-nr", action="store_false", dest="resolver",
        help="disable creating resolver files"
    )

    parser.set_defaults(**config.DEFAULTS)
    return parser.parse_args(args, namespace=config)


def main():  # pragma: no cover
    return DevNS(parse_args()).run()


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
