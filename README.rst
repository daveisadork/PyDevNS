PyDevNS
=======
A pure Python DNS server for developers.

How to use the thing::
    usage: devns [-h] [--verbose | --quiet] [--host HOST] [--port PORT]
                 [--address ADDRESS] [--no-resolver]
                 [domains]

    positional arguments:
      domains             domains to create resolver files for

    optional arguments:
      -h, --help          show this help message and exit
      --verbose, -v       verbose output
      --quiet, -q         quiet mode
      --host HOST         address to listen on
      --port PORT         port to listen on
      --address ADDRESS   IP address to respond with
      --no-resolver, -nr  don't put files in /etc/resolver
