from __future__ import (
    absolute_import, print_function, unicode_literals
)
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
        A = 1            # a host address
        NS = 2           # an authoritative name server
        MD = 3           # a mail destination (OBSOLETE - use MX)
        MF = 4           # a mail forwarder (OBSOLETE - use MX)
        CNAME = 5        # the canonical name for an alias
        SOA = 6          # marks the start of a zone of authority
        MB = 7           # a mailbox domain name (EXPERIMENTAL)
        MG = 8           # a mail group member (EXPERIMENTAL)
        MR = 9           # a mail rename domain name (EXPERIMENTAL)
        NULL = 10        # a null RR (EXPERIMENTAL)
        WKS = 11         # a well known service description
        PTR = 12         # a domain name pointer
        HINFO = 13       # host information
        MINFO = 14       # mailbox or mail list information
        MX = 15          # mail exchange
        TXT = 16         # text strings
        RP = 17          # for Responsible Person
        AFSDB = 18       # for AFS Data Base location
        X25 = 19         # for X.25 PSDN address
        ISDN = 20        # for ISDN address
        RT = 21          # for Route Through
        NSAP = 22        # for NSAP address, NSAP style A record
        NSAP_PTR = 23    # for domain name pointer, NSAP style
        SIG = 24         # for security signature
        KEY = 25         # for security key
        PX = 26          # X.400 mail mapping information
        GPOS = 27        # Geographical Position
        AAAA = 28        # IP6 Address
        LOC = 29         # Location Information
        NXT = 30         # Next Domain (OBSOLETE)
        EID = 31         # Endpoint Identifier
        NIMLOC = 32      # Nimrod Locator
        SRV = 33         # Server Selection
        ATMA = 34        # ATM Address
        NAPTR = 35       # Naming Authority Pointer
        KX = 36          # Key Exchanger
        CERT = 37        # CERT
        A6 = 38          # A6 (OBSOLETE - use AAAA)
        DNAME = 39       # DNAME
        SINK = 40        # SINK
        OPT = 41         # OPT
        APL = 42         # APL
        DS = 43          # Delegation Signer
        SSHFP = 44       # SSH Key Fingerprint
        IPSECKEY = 45    # IPSECKEY
        RRSIG = 46       # RRSIG
        NSEC = 47        # NSEC
        DNSKEY = 48      # DNSKEY
        DHCID = 49       # DHCID
        NSEC3 = 50       # NSEC3
        NSEC3PARAM = 51  # NSEC3PARAM
        TLSA = 52        # TLSA
        SMIMEA = 53      # S/MIME cert association
        HIP = 55         # Host Identity Protocol
        NINFO = 56       # NINFO
        RKEY = 57        # RKEY
        TALINK = 58      # Trust Anchor LINK
        CDS = 59         # Child DS
        CDNSKEY = 60     # DNSKEY(s) the Child wants reflected in DS
        OPENPGPKEY = 61  # OpenPGP Key
        CSYNC = 62       # Child-To-Parent Synchronization
        SPF = 99
        UINFO = 100
        UID = 101
        GID = 102
        UNSPEC = 103
        NID = 104
        L32 = 105
        L64 = 106
        LP = 107
        EUI48 = 108      # an EUI-48 address
        EUI64 = 109      # an EUI-64 address
        TKEY = 249       # Transaction Key
        TSIG = 250       # Transaction Signature
        IXFR = 251       # incremental transfer
        AXFR = 252       # transfer of an entire zone
        MAILB = 253      # mailbox-related RRs (MB, MG or MR)
        MAILA = 254      # mail agent RRs (OBSOLETE - see MX)
        # * = 255        # A request for all records the server/cache has available
        URI = 256        # URI
        CAA = 257        # Certification Authority Restriction
        AVC = 258        # Application Visibility and Control
        TA = 32768       # DNSSEC Trust Authorities
        DLV = 32769      # DNSSEC Lookaside Validation


def bytes_to_int(value):
    return int("".join("%x" % _intify(x) for x in value), 16)


def _bytes(args):  # pragma: no cover
    return b"".join(chr(i) for i in args)


if bytes is not str:  # pragma: no cover
    _bytes = bytes  # noqa


def int_to_bytes(value, length=4):
    fmt = ("%%0%dx" % length) % value
    ints = tuple(
        int(fmt[x:x + 2], 16) for x in range(0, len(fmt), 2)
    )
    return _bytes(ints)


def _intify(value):
    if not isinstance(value, int):
        value = ord(value)
    return value


class Header(object):
    def __init__(self, id, qr=0, opcode=0, aa=0, tc=0, rd=0, ra=0, z=0, ad=0,
                 cd=0, rcode=0, query=0, answer=0, authority=0, additional=0):
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.z = z
        self.ad = ad
        self.cd = cd
        self.rcode = rcode
        self.query = query
        self.answer = answer
        self.authority = authority
        self.additional = additional

    @property
    def opcode_str(self):
        for opcode in dir(DNS.OpCode):
            if getattr(DNS.OpCode, opcode, None) == self.opcode:
                break
        else:
            opcode = str(self.opcode)
        return opcode

    @property
    def rcode_str(self):
        for rcode in dir(DNS.RCode):
            if getattr(DNS.RCode, rcode, None) == self.rcode:
                break
        else:
            rcode = str(self.rcode)
        return rcode

    @property
    def flags(self):
        return (
            ("qr", self.qr),
            ("aa", self.aa),
            ("tc", self.tc),
            ("rd", self.rd),
            ("ra", self.ra),
            ("z", self.z),
            ("ad", self.ad),
            ("cd", self.cd),
        )

    @classmethod
    def from_bytes(cls, data):
        flags = format(bytes_to_int(data[2:4]), "016b")
        return cls(
            id=bytes_to_int(data[:2]),
            qr=int(flags[0], 2),   # Query
            opcode=int(flags[1:5], 2),
            aa=int(flags[5], 2),   # Authoritative Answer
            tc=int(flags[6], 2),   # Truncated Response
            rd=int(flags[7], 2),   # Recursion Desired
            ra=int(flags[8], 2),   # Recursion Available
            z=int(flags[9], 2),    # Reserved
            ad=int(flags[10], 2),  # Authentic Data
            cd=int(flags[11], 2),  # Checking Disabled
            rcode=int(flags[12:], 2),
            query=bytes_to_int(data[4:6]),
            answer=bytes_to_int(data[6:8]),
            authority=bytes_to_int(data[8:10]),
            additional=bytes_to_int(data[10:12]),
        )

    def __str__(self):
        return "\n".join((
            ";; ->>HEADER<<- opcode: %s, status: %s, id: %s",
            ";; flags: %s; QUERY: %s, ANSWER: %s, AUTHORITY: %s, ADDITIONAL: %s",
        )) % (
            self.opcode_str.upper(), self.rcode_str.upper(), self.id,
            " ".join(flag for flag, value in self.flags if value),
            self.query, self.answer, self.authority, self.additional
        )

    def __repr__(self):
        args = (
            ("id", self.id),
            ("qr", self.qr),
            ("opcode", self.opcode),
            ("aa", self.aa),
            ("tc", self.tc),
            ("rd", self.rd),
            ("ra", self.ra),
            ("z", self.z),
            ("ad", self.ad),
            ("cd", self.cd),
            ("rcode", self.rcode),
            ("query", self.query),
            ("answer", self.answer),
            ("authority", self.authority),
            ("additional", self.additional),
        )
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("=".join((k, repr(v))) for k, v in args)
        )

    def to_bytes(self):
        header = int("".join((
            format(self.qr, "b"),        # QR: Response
            format(self.opcode, "04b"),  # Opcode
            format(self.aa, "b"),        # Authoritative Answer
            format(self.tc, "b"),        # Truncated Response
            format(self.rd, "b"),        # Recursion Desired
            format(self.ra, "b"),        # Recursion Available (should match RD)
            format(self.z, "b"),         # Reserved
            format(self.ad, "b"),        # Authentic Data
            format(self.cd, "b"),        # Checking Disabled
            format(self.rcode, "04b")    # status: NOERROR
        )), 2)
        return b"".join((
            int_to_bytes(self.id),          # ID
            int_to_bytes(header),
            int_to_bytes(self.query),       # QUERY: 1
            int_to_bytes(self.answer),      # ANSWER: 1
            int_to_bytes(self.authority),   # AUTHORITY: 0
            int_to_bytes(self.additional),  # ADDITIONAL: 0
        ))


class Query(object):
    def __init__(self, rrtype, labels, qclass=1):
        self.rrtype = rrtype
        self.labels = labels
        self.qclass = qclass

    @property
    def rrtype_str(self):
        for rrtype in dir(DNS.RRType):
            if getattr(DNS.RRType, rrtype, None) == self.rrtype:
                break
        else:
            rrtype = str(self.rrtype)
        return rrtype

    @property
    def qclass_str(self):
        if self.qclass == 1:
            return "IN"
        return str(self.qclass)

    @property
    def domain(self):
        return ".".join(self.labels)

    @classmethod
    def from_bytes(cls, data):
        ini = 12
        lon = _intify(data[ini])
        labels = []
        while lon != 0:
            part = data[ini + 1:ini + lon + 1]
            labels.append(part.decode("latin-1"))
            ini += lon + 1
            lon = _intify(data[ini])
        rrtype = bytes_to_int(data[ini + 1:ini + 3])
        qclass = bytes_to_int(data[ini + 3:ini + 5])
        return cls(rrtype, tuple(labels), qclass)

    def to_bytes(self):
        parts = []
        for label in self.labels:
            parts.extend(chr(len(label)))
            parts.append(label)
        parts = "".join(parts).encode("latin-1")
        parts += b"".join((
            b"\x00", int_to_bytes(self.rrtype), int_to_bytes(self.qclass)
        ))
        return parts

    def __repr__(self):
        return "%s(rrtype=%r, labels=%r, qclass=%r)" % (
            type(self).__name__, self.rrtype, self.labels, self.qclass
        )

    def __str__(self):
        return "\n".join((
            ";; QUESTION SECTION",
            ";%s.\t\t  %s\t  %s" % (
                self.domain, self.qclass_str, self.rrtype_str
            )
        ))


class Request(object):
    def __init__(self, header, query):
        self.header = header
        self.query = query

    @classmethod
    def from_bytes(cls, data):
        return cls(
            header=Header.from_bytes(data),
            query=Query.from_bytes(data)
        )

    def to_bytes(self):
        return b"".join((self.header.to_bytes(), self.query.to_bytes()))

    def __str__(self):
        return "%s\n\n%s\n" % (self.header, self.query)

    def __repr__(self):
        return "%s(header=%r, query=%r)" % (
            type(self).__name__, self.header, self.query
        )


class Response(Request):
    def __init__(self, header, query, address, ttl=60):
        super(Response, self).__init__(header, query)
        self.address = address
        self.ttl = ttl

    def to_bytes(self):
        return b"".join((
            super(Response, self).to_bytes(),
            b"\xc0\x0c",                      # Pointer/Offset
            int_to_bytes(self.query.rrtype),  # TYPE: A
            int_to_bytes(self.query.qclass),  # CLASS: IN
            int_to_bytes(self.ttl, 8),        # TTL: 60
            int_to_bytes(4),                  # RDLENGTH: 4 octets
            _bytes(int(octet) for octet in self.address.split('.')),
        ))

    def __str__(self):
        answer = "\n".join((
            ";; ANSWER SECTION",
            "%s.\t\t  %s\t  %s\t  %s\t  %s" % (
                self.query.domain, self.ttl, self.query.qclass_str.upper(),
                self.query.rrtype_str.upper(), self.address
            )
        ))
        return "%s\n%s\n" % (super(Response, self).__str__(), answer)

    def __repr__(self):
        return "%s(header=%r, query=%r, address=%r, ttl=%r)" % (
            type(self).__name__, self.header, self.query, self.address, self.ttl
        )
