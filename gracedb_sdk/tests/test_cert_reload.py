"""Tests for :mod:`gracedb_sdk.cert_reload`."""
from datetime import datetime
from ssl import SSLContext, VerifyMode

from cryptography.x509 import (
    CertificateBuilder, DNSName, Name, NameAttribute, random_serial_number,
    SubjectAlternativeName)
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.primitives.serialization import (
    Encoding, NoEncryption, PrivateFormat)
from cryptography.hazmat.primitives.hashes import SHA256
import pytest
from pytest_httpserver import HTTPServer

from .. import Client


@pytest.fixture
def backend():
    return default_backend()


@pytest.fixture
def client_key(backend):
    """Generate client RSA key."""
    return generate_private_key(65537, 2048, backend)


@pytest.fixture
def server_key(backend):
    """Generate server RSA key."""
    return generate_private_key(65537, 2048, backend)


@pytest.fixture
def client_cert(client_key, backend):
    """Generate client certificate."""
    subject = issuer = Name([
        NameAttribute(NameOID.COMMON_NAME, 'example.org'),
        NameAttribute(NameOID.ORGANIZATION_NAME, 'Alice A. Client')
    ])
    return CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).serial_number(
        random_serial_number()
    ).public_key(
        client_key.public_key()
    ).not_valid_before(
        datetime.fromisoformat('2019-01-01')
    ).not_valid_after(
        datetime.fromisoformat('2019-01-10')
    ).add_extension(
        SubjectAlternativeName([DNSName('localhost')]),
        critical=False
    ).sign(
        client_key, SHA256(), backend
    )


@pytest.fixture
def server_cert(server_key, backend):
    """Generate server certificate."""
    subject = issuer = Name([
        NameAttribute(NameOID.COMMON_NAME, 'localhost'),
        NameAttribute(NameOID.ORGANIZATION_NAME, 'Bob B. Server')
    ])
    return CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).serial_number(
        random_serial_number()
    ).public_key(
        server_key.public_key()
    ).not_valid_before(
        datetime.fromisoformat('2018-01-01')
    ).not_valid_after(
        datetime.fromisoformat('2020-01-01')
    ).add_extension(
        SubjectAlternativeName([DNSName('localhost')]),
        critical=False
    ).sign(
        server_key, SHA256(), backend
    )


@pytest.fixture
def client_key_file(client_key, tmpdir):
    """Generate client key file."""
    filename = str(tmpdir / 'client_key.pem')
    with open(filename, 'wb') as f:
        f.write(client_key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))
    return filename


@pytest.fixture
def server_key_file(server_key, tmpdir):
    """Generate server key file."""
    filename = str(tmpdir / 'server_key.pem')
    with open(filename, 'wb') as f:
        f.write(server_key.private_bytes(
            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))
    return filename


@pytest.fixture
def client_cert_file(client_cert, tmpdir):
    """Generate client certificate file."""
    filename = str(tmpdir / 'client_cert.pem')
    with open(filename, 'wb') as f:
        f.write(client_cert.public_bytes(Encoding.PEM))
    return filename


@pytest.fixture
def server_cert_file(server_cert, tmpdir):
    """Generate server certificate file."""
    filename = str(tmpdir / 'server_cert.pem')
    with open(filename, 'wb') as f:
        f.write(server_cert.public_bytes(Encoding.PEM))
    return filename


@pytest.fixture
def server(socket_enabled, server_cert_file, server_key_file):
    """Run test https server."""
    context = SSLContext()
    context.load_cert_chain(server_cert_file, server_key_file)
    context.verify_mode = VerifyMode.CERT_NONE
    with HTTPServer(ssl_context=context) as server:
        server.expect_request('/').respond_with_json({'foo': 'bar'})
        yield server


@pytest.fixture
def client(server, client_cert_file, client_key_file, server_cert_file):
    """Create test client."""
    url = server.url_for('/')
    cert = (client_cert_file, client_key_file)
    with Client(url, cert=cert, cert_reload=True) as client:
        client.verify = server_cert_file
        yield client


def test_cert_reload(client, freezer):
    url = client.url

    # Test 1: significantly before expiration time, still valid
    freezer.move_to('2019-01-02')
    assert client.get(url).json() == {'foo': 'bar'}
    pool1 = client.get_adapter(url=url).poolmanager.connection_from_url(url)
    conn1 = pool1.pool.queue[-1]

    # Test 2: > cert_reload_timeout seconds before expiration time, still valid
    freezer.move_to('2019-01-09T23:54:59')
    assert client.get(client.url).json() == {'foo': 'bar'}
    pool2 = client.get_adapter(url=url).poolmanager.connection_from_url(url)
    conn2 = pool2.pool.queue[-1]
    assert pool1 is pool2
    assert conn1 is conn2

    # Test 3: < cert_reload_timeout seconds before expiration time, invalid
    freezer.move_to('2019-01-10')
    assert client.get(client.url).json() == {'foo': 'bar'}
    pool3 = client.get_adapter(url=url).poolmanager.connection_from_url(url)
    conn3 = pool3.pool.queue[-1]
    assert pool1 is pool3
    assert conn1 is not conn3
