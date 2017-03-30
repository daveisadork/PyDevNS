PyDevNS
=======

.. image:: https://img.shields.io/pypi/v/devns.svg
    :target: https://pypi.python.org/pypi/devns

.. image:: https://img.shields.io/pypi/l/devns.svg
    :target: https://pypi.python.org/pypi/devns

.. image:: https://img.shields.io/pypi/wheel/devns.svg
    :target: https://pypi.python.org/pypi/devns

.. image:: https://img.shields.io/pypi/pyversions/devns.svg
    :target: https://pypi.python.org/pypi/devns

.. image:: https://travis-ci.org/daveisadork/PyDevNS.svg?branch=master
    :target: https://travis-ci.org/daveisadork/PyDevNS

.. image:: https://codecov.io/gh/daveisadork/PyDevNS/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/daveisadork/PyDevNS

PyDevNS is a pure Python DNS server for developers. You know how you need
a domain name to use for interacting with your app locally? Well, this is the
tool for you.

Installation
------------

``pip install devns``

Hey, not everything has to be hard.

Rationale
---------
I know what you're thinking:

   Dude, what? I just put ``local.dev`` in my ``/etc/hosts`` file.

That's all well and good, but what about when you need ``local.dev`` and
``*.local.co``?

   There's like a million things out there that do this. I could use
   ``dnsmasq``, or one of the other 40 random Python "dev DNS" servers you
   probably stole your implementation from.

OK, ``dnsmasq`` kind of seems like overkill, but what about when you need
``local.dev`` or ``reallycoolprogrammer.local.dev`` to work from inside a 
docker container?

   Well then I just make ``dnsmasq`` resolve it to my real IP instead of
   ``127.0.0.1``. 

So you edit the config and restart ``dnsmasq`` every time you move from home,
to the coffee shop, to the office, wherever...

   That is kind of a pain, now that you mention it...

Thought so.

Default Behavior
----------------

If you run ``devns`` with no arguments, the server will start, bind to
``0.0.0.0`` with a random port and try to discover a suitable IP address to use
for resolving any incoming DNS requests. It literally does not care what domain
you ask for, it always responds and always with the same IP, hopefully the IP
address of your actual network interface (e.g. ``192.168.1.52`` or whatever).
It tries to figure that out on its own, and I think it does a pretty good job
of it.

   But then how do I make DNS queries go to it, especially if it's using a
   random port every time it runs?

Glad you asked. It'll also try to write a file to ``/etc/resolver/dev``, which
if your OS supports such things, would tell it to send any DNS queries for
domains ending it ``.dev`` to ``devns``.

   But wouldn't I need to...

Run it with ``sudo`` to do that? Yeah probably, unless your system is insane
and just lets anybody write to ``/etc`` all willy nilly, in which case you have
bigger problems than getting ``local.dev`` to resolve to something sensible.

   Don't I have to restart it every time my IP changes, just like ``dnsmasq``?

No, there's a configurable TTL associated with the address ``devns`` uses in
its responses. By default, that's 5 minutes. If a query comes in and the
address was last confirmed more than 5 minutes prior, it'll try to rediscover
it. That should cover most cases of relocating from one spot to another.

Examples
--------
Run the server with a random port and auto-configured resolver for ``.dev``
resolving to a sensible, auto-detected IP address:

   ``sudo devns``

Rediscover the response address every 15 minutes instead of 5:

   ``sudo devns --ttl 900``

Listen on port ``53535`` without writing any resolver files:

  ``devns --port 53535 --no-resolver``

Write the resolver files to ``/usr/local/etc/resolver`` instead of
``/etc/resolver``:

  ``devns --resolver-dir /usr/local/etc/resolver``

Respond to all queries with ``172.24.3.1``, and ignore the TTL:

  ``sudo devns --address 172.24.3.1``

Listen on port ``53535``, write config files for ``.dev`` and ``.local.co``:

  ``sudo devns --port 53535 --domains dev local.co``

Bind to a random port on ``127.0.0.1``, and make a lot of noise:

   ``sudo devns --host 127.0.0.1 -vvv``

Notes/Caveats
-------------
If you have entries in your ``/etc/hosts`` for any domains you want to use with
``devns``, you'll have to remove those. That's all.

Usage
-----
Here's what ``devns --help`` gets you:

.. code-block::

    usage: devns [-h] [--version] [--verbose | --quiet]
                 [--address ADDRESS | --ttl SECONDS] [--host HOST] [--port PORT]
                 [--domains [DOMAIN [DOMAIN ...]]] [--resolver-dir DIRECTORY]
                 [--no-resolver]

    PyDevNS - A DNS server for developers.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show version and exit

    Logging:
      --verbose, -v         verbose output
      --quiet, -q           quiet mode

    Address:
      --address ADDRESS, -a ADDRESS
                            IP address to respond with
      --ttl SECONDS, -t SECONDS
                            how often to refresh the address

    Network:
      --host HOST, -H HOST  address to listen on
      --port PORT, -p PORT  port to listen on

    Resolver:
      --domains [DOMAIN [DOMAIN ...]], -d [DOMAIN [DOMAIN ...]]
                            domains to create resolver files for
      --resolver-dir DIRECTORY, -rd DIRECTORY
                            where to put resolver files
      --no-resolver, -nr    disable creating resolver files
