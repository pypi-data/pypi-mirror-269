from finalsa.s3.client import (
    S3Client,
    S3ClientImpl,
    S3ClientTest,
    __version__
)
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def test_version():
    assert __version__ is not None


def test_client():
    assert S3Client is not None

def test_client_impl():
    assert S3ClientImpl is not None 

def test_client_test():
    client = S3ClientTest()
    assert client is not None

def test_client_get_object():
    client = S3ClientTest()
    client.put_object("bucket", "key", b"data")
    assert client.get_object("bucket", "key") == b"data"

def test_client_put_object():
    client = S3ClientTest()
    client.put_object("bucket", "key", b"data")
    assert client.get_object("bucket", "key") == b"data"

def test_client_delete_object():
    client = S3ClientTest()
    client.put_object("bucket", "key", b"data")
    client.delete_object("bucket", "key")

    assert "key" not in client.list_objects("bucket")

def test_client_list_objects():
    client = S3ClientTest()
    client.put_object("bucket", "key", b"data")
    client.put_object("bucket", "key2", b"data")

    assert set(client.list_objects("bucket")) == {"key", "key2"}
    