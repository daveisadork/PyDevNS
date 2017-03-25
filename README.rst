PyDevNS
=======

.. image:: https://travis-ci.org/daveisadork/PyDevNS.svg?branch=master
    :target: https://travis-ci.org/daveisadork/PyDevNS

.. image:: https://codecov.io/gh/daveisadork/PyDevNS/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/daveisadork/PyDevNS

PyDevNS is a pure Python DNS server for developers. You know how you need
a domain name to use for interact with your app locally? Well, this is the tool
for you.

----------

I know what you're thinking

   Dude, what? I just put ``local.dev`` in my ``/etc/hosts`` file.

Well, that's all well and good, but what about when you need ``local.dev`` and
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

Examples
--------
Run the server with a random port and auto-configured resolver for ``.dev``
resolving to a sensible, auto-detected IP address:

   ``sudo devns``

Listen on port 53535 without writing any resolver files:

  ``devns --port 53535 --no-resolver``

Respond with a specific IP every time instead of an auto discovered one:

  ``sudo devns --address 172.24.3.1``

Listen on port 53535, write config files for `.dev` and `.local.co`:

  ``sudo devns --port 53535 --domains dev local.co``

Bind to a random port on `127.0.0.1`, and make a lot of noise:

   ``sudo devns --host 127.0.0.1 -vvv``

----------

Here's what ``devns --help`` gets you:

usage: devns [-h] [--verbose | --quiet] [--host HOST] [--port PORT]
             [--address ADDRESS]
             [--no-resolver | --domains [DOMAIN [DOMAIN ...]]]

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         verbose output
  --quiet, -q           quiet mode
  --host HOST           address to listen on
  --port PORT           port to listen on
  --address ADDRESS     IP address to respond with
  --no-resolver, -nr    don't put files in /etc/resolver
  --domains [DOMAIN [DOMAIN ...]]
                        domains to create resolver files for
