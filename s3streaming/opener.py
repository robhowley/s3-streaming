
import boto3
from urlparse import urlparse
from contextlib import contextmanager
from s3streaming.stream import StreamingBodyFileobj, deserialize, compression


__all__ = ['s3_open']


def from_s3_uri(s3_uri):
    parsed = urlparse(s3_uri)
    key = parsed.path
    return dict(Bucket=parsed.netloc, Key=key[1:] if key else '')


@contextmanager
def s3_open(s3_uri, deserializer=deserialize.none, compression=compression.none):
    deserializer, compression = deserializer or (lambda s: s), compression or (lambda s: s)

    body = StreamingBodyFileobj(boto3.client('s3').get_object(**from_s3_uri(s3_uri))['Body'])
    yield deserializer(compression(body))
