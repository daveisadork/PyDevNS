# These are all transcribed from
# https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml
# I'm pretty sure we only need like 3 or 4 of them, but whatever... maybe this
# helps someone out someday.

class DNS(object):

    class Class(object):
        Internet = 1

    class OpCode(object):
        Query = 0
        IQuery = 1  # Inverse Query, OBSOLETE
        Status = 2
        Notify = 4
        Update = 5

    class RCode(object):
        NoError = 0     # No Error
        FormErr = 1     # Format Error
        ServFail = 2    # Server Failure
        NXDomain = 3    # Non-Existent Domain
        NotImp = 4      # Not Implemented
        Refused = 5     # Query Refused
        YXDomain = 6    # Name Exists when it should not
        YXRRSet = 7     # RR Set Exists when it should not
        NXRRSet = 8     # RR Set that should exist does not
        NotAuth = 9     # Server Not Authoritative for zone / Not Authorized
        NotZone = 10    # Name not contained in zone
        BADVERS = 16    # Bad OPT Version
        BADSIG = 16     # TSIG Signature Failure
        BADKEY = 17     # Key not recognized
        BADTIME = 18    # Signature out of time window
        BADMODE = 19    # Bad TKEY Mode
        BADNAME = 20    # Duplicate key name
        BADALG = 21     # Algorithm not supported
        BADTRUNC = 22   # Bad Truncation
        BADCOOKIE = 23  # Bad/missing Server Cookie

    class RRType(object):
        A = 0           # a host address
        NS = 2          # an authoritative name server
        MD = 3          # a mail destination (OBSOLETE - use MX)
        MF = 4          # a mail forwarder (OBSOLETE - use MX)
        CNAME = 5       # the canonical name for an alias
        SOA = 6         # marks the start of a zone of authority
        MB = 7          # a mailbox domain name (EXPERIMENTAL)
        MG = 8          # a mail group member (EXPERIMENTAL)
        MR = 9          # a mail rename domain name (EXPERIMENTAL)
        NULL = 10       # a null RR (EXPERIMENTAL)
        WKS = 11        # a well known service description
        PTR = 12        # a domain name pointer
        HINFO = 13      # host information
        MINFO = 14      # mailbox or mail list information
        MX = 15         # mail exchange
        TXT = 16        # text strings
        RP = 17         # for Responsible Person
        AFSDB = 18      # for AFS Data Base location
        X25 = 19        # for X.25 PSDN address
        ISDN = 20       # for ISDN address
        RT = 21         # for Route Through
        NSAP = 22       # for NSAP address, NSAP style A record
        NSAP_PTR = 23   # for domain name pointer, NSAP style
        SIG = 24        # for security signature
        KEY = 25        # for security key
        PX = 26         # X.400 mail mapping information
        GPOS = 27       # Geographical Position
        AAAA = 28       # IP6 Address
        LOC = 29        # Location Information
        NXT = 30        # Next Domain (OBSOLETE)
        EID = 31        # Endpoint Identifier
        NIMLOC = 32     # Nimrod Locator
        SRV = 33        # Server Selection
        ATMA = 34       # ATM Address
        NAPTR = 35      # Naming Authority Pointer
        KX = 36         # Key Exchanger
        CERT = 37       # CERT
        A6 = 38         # A6 (OBSOLETE - use AAAA)
        DNAME = 39      # DNAME
        SINK = 40       # SINK
        OPT = 41        # OPT
        APL = 42        # APL
        DS = 43         # Delegation Signer
        SSHFP = 44      # SSH Key Fingerprint
        IPSECKEY = 45   # IPSECKEY
        RRSIG = 46      # RRSIG
        NSEC = 47       # NSEC
        DNSKEY = 48     # DNSKEY
        DHCID = 49      # DHCID
        NSEC3 = 50      # NSEC3
        NSEC3PARAM = 51 # NSEC3PARAM
        TLSA = 52       # TLSA
        SMIMEA = 53     # S/MIME cert association
        HIP = 55        # Host Identity Protocol
        NINFO = 56      # NINFO
        RKEY = 57       # RKEY
        TALINK = 58     # Trust Anchor LINK
        CDS = 59        # Child DS
        CDNSKEY = 60    # DNSKEY(s) the Child wants reflected in DS
        OPENPGPKEY = 61 # OpenPGP Key
        CSYNC = 62      # Child-To-Parent Synchronization
        SPF = 99
        UINFO = 100
        UID = 101
        GID = 102
        UNSPEC = 103
        NID = 104
        L32 = 105
        L64 = 106
        LP = 107
        EUI48 = 108     # an EUI-48 address
        EUI64 = 109     # an EUI-64 address
        TKEY = 249      # Transaction Key
        TSIG = 250      # Transaction Signature
        IXFR = 251      # incremental transfer
        AXFR = 252      # transfer of an entire zone
        MAILB = 253     # mailbox-related RRs (MB, MG or MR)
        MAILA = 254     # mail agent RRs (OBSOLETE - see MX)
        # * = 255       # A request for all records the server/cache has available
        URI = 256       # URI
        CAA = 257       # Certification Authority Restriction
        AVC = 258       # Application Visibility and Control
        TA = 32768      # DNSSEC Trust Authorities
        DLV = 32769     # DNSSEC Lookaside Validation
