import pytest
from devns.dns import _intify, Header, Query, Request, Response

header = Header(
    id=56235, qr=0, opcode=0, aa=0, tc=0, rd=0, ra=0, z=0, ad=0, cd=1, rcode=0,
    query=1, answer=0, authority=0, additional=0
)
query = Query(rrtype=1, labels=('local', 'dev'), qclass=1)
request = Request(header, query)
response = Response(header, query, "1.2.3.4", 60)


@pytest.mark.parametrize("instance, expected", [
    (header, "Header(id=56235, qr=0, opcode=0, aa=0, tc=0, rd=0, ra=0, z=0, ad=0, cd=1, rcode=0, query=1, answer=0, authority=0, additional=0)"),  # noqa
    (query, "Query(rrtype=1, labels=('local', 'dev'), qclass=1)"),
    (request, "Request(header=Header(id=56235, qr=0, opcode=0, aa=0, tc=0, rd=0, ra=0, z=0, ad=0, cd=1, rcode=0, query=1, answer=0, authority=0, additional=0), query=Query(rrtype=1, labels=('local', 'dev'), qclass=1))"),  # noqa
    (response, "Response(header=Header(id=56235, qr=0, opcode=0, aa=0, tc=0, rd=0, ra=0, z=0, ad=0, cd=1, rcode=0, query=1, answer=0, authority=0, additional=0), query=Query(rrtype=1, labels=('local', 'dev'), qclass=1), address='1.2.3.4', ttl=60)"),  # noqa
])
def test_repr(instance, expected):
    assert repr(instance) == expected


@pytest.mark.parametrize("instance, expected", [
    (header, ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 56235\n;; flags: cd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0"),  # noqa
    (query, ";; QUESTION SECTION\n;local.dev.\t\t  IN\t  A"),
    (request, ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 56235\n;; flags: cd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0\n\n;; QUESTION SECTION\n;local.dev.\t\t  IN\t  A\n"),  # noqa
    (response, ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 56235\n;; flags: cd; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 0\n\n;; QUESTION SECTION\n;local.dev.\t\t  IN\t  A\n\n;; ANSWER SECTION\nlocal.dev.\t\t  60\t  IN\t  A\t  1.2.3.4\n"),  # noqa
])
def test_str(instance, expected):
    print(repr(str(instance)))
    assert str(instance) == expected


def test_nonstandard_query_attributes():
    query = Query(rrtype=-1, labels=('local', 'dev'), qclass=-1)
    assert query.rrtype_str == "-1"
    assert query.qclass_str == "-1"


def test_nonstandard_header_attributes():
    header = Header(
        id=56235, qr=0, opcode=-1, aa=0, tc=0, rd=0, ra=0, z=0, ad=0, cd=1,
        rcode=-1, query=1, answer=0, authority=0, additional=0
    )
    assert header.opcode_str == "-1"
    assert header.rcode_str == "-1"


@pytest.mark.parametrize("value, expected", [
    (1, 1),
    ("1", 49),
    (b"\x01", 1)
])
def test_intify(value, expected):
    assert _intify(value) == expected
