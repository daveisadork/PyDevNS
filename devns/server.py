from __future__ import (
    absolute_import, print_function, unicode_literals
)
from builtins import *  # noqa

import os
import socket
import logging
import functools
import subprocess
from datetime import datetime

from . import config, DNS
from contextlib import contextmanager


logger = logging.getLogger(__name__)


def interruptable(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            logger.info("User pressed Control+C, shutting down")
            return 0

    return decorator


def _intify(value):
    if not isinstance(value, int):
        value = ord(value)
    return value


class DevNS(object):
    def __init__(self, config=config, **kwargs):
        self.config = config
        self.config.update(kwargs)
        self.connection = None
        self._address = None
        self._address_last_updated = datetime.utcnow()

    def _choose_address(self, addresses):
        logger.debug("Selecting the best IP from candidates %r", addresses)
        possible = []
        if not isinstance(addresses, list):
            addresses = [addresses]

        for address in addresses:
            try:
                ip = [int(p) for p in address.split(".")]
                assert ip[0] in (192, 172, 127, 10)
                assert ip[3] < 255
                if ip[0] == 192:
                    assert ip[1] == 168
                if ip[0] == 172:
                    assert ip[1] > 15
                    assert ip[1] < 32
                possible.append(ip)
                logger.debug("Considering %s", address)
            except:
                logger.debug("Skipping %s", address)
        possible = [".".join([str(part) for part in parts]) for parts in sorted(
            possible,
            key=lambda p: "{0}-{1}".format(
                0 if p[0] == 127 else 1, p[-1]
            )
        )]
        if possible:
            address = possible[-1]
            logger.debug("Selected IP address %s", address)
            return address
        else:
            logger.warning("Found no suitable IP addresses in %r", addresses)

    def _get_address_by_hostname(self):
        try:
            logger.debug("Attempting to determine response IP from hostname")
            hostname = socket.getfqdn()
            logger.debug("Resolving hostname %r", hostname)
            return self._choose_address(socket.gethostbyname(hostname))
        except Exception as e:
            logger.warning("Unable to resolve %r: %s", hostname, e)

    def _get_address_by_ifconfig(self):
        logger.debug("Attempting to determine response IP from ifconfig")
        addresses = []
        output = subprocess.check_output(("ifconfig", ))
        if not isinstance(output, str):
            output = output.decode("latin-1")
        for line in output.split("\n"):
            try:
                parts = line.strip().split(" ")
                assert parts[0] == "inet"
                address = parts[1].split(":")[-1]
                addresses.append(address)
            except:
                continue
        return self._choose_address(addresses)

    @property
    def _address_age(self):
        if self.config.address:
            return 0
        delta = datetime.utcnow() - self._address_last_updated
        return delta.days * 86400 + delta.seconds

    @property
    def address(self):
        if not self._address:
            logger.debug("Address not set, refreshing")
            self.address = self.config.address
        elif self._address_age > self.config.ttl:
            logger.debug("Address is stale, refreshing")
            self.address = self.config.address
        return self._address

    @address.setter
    def address(self, address):
        address = address or self._get_address_by_ifconfig()
        address = address or self._get_address_by_hostname()
        if not address:
            logger.critical(
                "Could not determine a suitable response IP address. Please "
                "specify one."
            )
            raise RuntimeError(
                "Could not determine a suitable response IP address. Please "
                "specify one."
            )
        self._address = address
        self._encoded_address = "".join(
            map(lambda x: chr(int(x)), address.split('.'))
        ).encode("latin-1")
        self._address_last_updated = datetime.utcnow()

    @contextmanager
    def bind(self):
        logger.debug("Opening socket")
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.debug("Setting socket timeout to 3.05 seconds")
        connection.settimeout(3.05)
        if self.config.port:
            logger.debug(
                "Attempting to bind to %s:%s",
                self.config.host,
                self.config.port
            )
        else:
            logger.debug(
                "Attempting to bind to %r with a random port", self.config.host
            )
        try:
            connection.bind((self.config.host, self.config.port))
            logger.debug(
                "Successfully bound to %s:%s", *connection.getsockname()
            )
            self.connection = connection
        except (socket.error, OverflowError, TypeError) as e:
            yield e
        else:
            yield self.connection
        finally:
            logger.debug("Closing socket")
            try:
                self.connection.close()
            except:
                pass

    def _build_response(self, data):
        labels = []
        opcode = (_intify(data[2]) >> 3) & 15  # This is so gross.
        if opcode != DNS.OpCode.Query:
            logger.warning("Ignoring unsupported opcode %s", opcode)
            return
        ini = 12
        lon = _intify(data[ini])
        while lon != 0:
            labels.append(data[ini+1:ini+lon+1].decode("latin-1"))
            ini += lon + 1
            lon = _intify(data[ini])
        domain = ".".join(labels)
        logger.info("QUERY %s IN A %s", domain, self.address)
        return b"".join((
            data[:2],
            b"\x81\x80",
            data[4:6],
            data[4:6],
            b"\x00\x00\x00\x00",  # Questions and Answers Counts
            data[12:],            # Original Domain Name Question
            b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04",
            self._encoded_address
        ))

    def _listen(self):
        logger.debug(
            "Ready to reply to incoming requests with %s", self.address
        )
        print("Listening on {0}:{1}".format(*self.connection.getsockname()))
        while True:
            try:
                query, client = self.connection.recvfrom(1024)
                logger.debug("Request from %s:%s", *client)
                response = self._build_response(query)
                if not response:
                    continue
                self.connection.sendto(response, client)
            except socket.error:
                continue

    @contextmanager
    def _resolver(self):
        resolvers = []
        resolver_config = "\n".join((
            "# generated by devns",
            "nameserver {0}",
            "port {1}"
        )).format(*self.connection.getsockname())

        try:
            if self.config.resolver:
                if not os.path.isdir(self.config.resolver_dir):
                    logger.info(
                        "resolver dir %r does not exist, creating it",
                        self.config.resolver_dir
                    )
                    os.mkdir(self.config.resolver_dir)
                for domain in self.config.domains:
                    path = os.path.join(self.config.resolver_dir, domain)
                    with open(path, "w") as resolver:
                        logger.debug("Writing resolver config to %s", path)
                        resolver.write(resolver_config)
                    resolvers.append(path)
        except IOError as e:
            yield e
        else:
            yield resolvers
        finally:
            while resolvers:
                resolver = resolvers.pop()
                logger.debug("Cleaning up resolver config %s", resolver)
                try:
                    os.unlink(resolver)
                except:
                    logger.error(
                        "Failed cleaning up resolver config %s", resolver
                    )

    @interruptable
    def _run(self):
        with self._resolver() as resolver:
            if isinstance(resolver, Exception):
                logger.critical(
                    "Failed trying to write resolver config: %s", resolver
                )
                return 3
            return self._listen()

    def run(self):
        with self.bind() as connection:
            if isinstance(connection, Exception):
                return 2
            return self._run()
