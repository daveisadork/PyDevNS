import logging

from six import iteritems


logging.basicConfig(
    format="[%(levelname)-8s] [%(name)-12s] %(message)s", level=logging.ERROR
)
logger = logging.getLogger(__name__)


class Config(object):
    DEFAULTS = dict(
        address=None,
        domains=("dev", ),
        host="",
        log_level=logging.ERROR,
        port=0,
        resolver=True,
        resolver_dir="/etc/resolver",
        ttl=300,
        verbosity=0,
    )

    def __init__(self):
        self._data = {}
        self.init_defaults()

    def init_defaults(self):
        self.update(self.DEFAULTS)

    def update(self, config):
        logger.debug("Updating configuration")
        for key in self.DEFAULTS:
            value = config.get(key, getattr(self, key))
            setattr(self, key, value)

    @property
    def address(self):
        return self._data.get("address", self.DEFAULTS["address"])

    @address.setter
    def address(self, address):
        logger.debug("Setting config.address to %r", address)
        self._data["address"] = address

    @property
    def domains(self):
        return self._data.get("domains", self.DEFAULTS["domains"])

    @domains.setter
    def domains(self, domains):
        logger.debug("Setting config.domains to %r", domains)
        if not isinstance(domains, (list, tuple)):
            domains = (domains, )
        self._data["domains"] = tuple(domains)

    @property
    def host(self):
        return self._data.get("host", self.DEFAULTS["host"])

    @host.setter
    def host(self, host):
        logger.debug("Setting config.host to %r", host)
        self._data["host"] = host

    @property
    def log_level(self):
        return logger.getEffectiveLevel()

    @log_level.setter
    def log_level(self, level):
        logger.debug("Setting config.log_level to %r", level)
        logging.getLogger().setLevel(level)
        logging._acquireLock()
        for name, _logger in iteritems(logging.Logger.manager.loggerDict):
            if isinstance(_logger, logging.PlaceHolder):
                continue
            _logger.setLevel(level)
        logging._releaseLock()

    @property
    def port(self):
        return self._data.get("port", self.DEFAULTS["port"])

    @port.setter
    def port(self, port):
        logger.debug("Setting config.port to %r", port)
        self._data["port"] = port

    @property
    def ttl(self):
        return self._data.get("ttl", self.DEFAULTS["ttl"])

    @ttl.setter
    def ttl(self, ttl):
        logger.debug("Setting config.ttl to %r", ttl)
        self._data["ttl"] = ttl

    @property
    def resolver(self):
        return self._data.get("resolver", self.DEFAULTS["resolver"])

    @resolver.setter
    def resolver(self, resolver):
        logger.debug("Setting config.resolver to %r", resolver)
        self._data["resolver"] = resolver

    @property
    def resolver_dir(self):
        return self._data.get("resolver_dir", self.DEFAULTS["resolver_dir"])

    @resolver_dir.setter
    def resolver_dir(self, resolver_dir):
        logger.debug("Setting config.resolver_dir to %r", resolver_dir)
        self._data["resolver_dir"] = resolver_dir

    @property
    def verbosity(self):
        return (40 - self.log_level) // 10

    @verbosity.setter
    def verbosity(self, verbosity):
        logger.debug("Setting config.verbosity to %r", verbosity)
        self.log_level = 40 - (verbosity * 10)
