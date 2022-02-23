from urllib.parse import urlparse
from contextlib import contextmanager
from s3streaming.stream import deserialize, compression


__all__ = ['s3_open']


def bucket_key_from_s3_uri(s3_uri):
    parsed = urlparse(s3_uri)
    key = parsed.path
    return dict(Bucket=parsed.netloc, Key=key[1:] if key else '')


@contextmanager
def s3_open(s3_uri, boto_session, deserializer=deserialize.none, compression=compression.none, params: dict=None):
    # combine params with dictionary from parsing uri and send to get_object
    body = boto_session.client('s3').get_object(**{**bucket_key_from_s3_uri(s3_uri),**(params if params is not None else {})})['Body']
    yield deserializer(compression(body._raw_stream))
