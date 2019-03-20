
import zlib
import json
from collections import namedtuple
from csv import DictReader, reader as csv_reader, excel_tab as csv_excel_tab


__all__ = ['deserialize', 'compression', 'StreamingBodyFileobj']


class FileLikeLineIterable(object):
    def __init__(self, wrapped_iterable):
        self.wrapped_iterable = wrapped_iterable

    def __iter__(self):
        for next_chunk in self.wrapped_iterable:
            yield next_chunk

    def next(self):
        return next(self.__iter__())

    def __next__(self):
        return self.next()

    def read(self, amt=1):
        return getattr(self.wrapped_iterable, 'read', self.readlines)(amt)

    def readlines(self, amt=1):
        return [self.next() for _ in range(amt)]


class StreamingBodyFileobj(FileLikeLineIterable):
    def __init__(self, streaming_body):
        self.streaming_body = streaming_body
        super(StreamingBodyFileobj, self).__init__(self.streaming_body._raw_stream)

    def __getattr__(self, item):
        return getattr(self.streaming_body._raw_stream, item)


class IterGzip(FileLikeLineIterable):
    @staticmethod
    def _scan_chunks(streaming_body):
        decompressor = zlib.decompressobj(32 + zlib.MAX_WBITS).decompress

        next_line = ''
        for chunk in streaming_body:
            line_broken = decompressor(chunk).split('\n')
            next_line += line_broken[0]
            if len(line_broken) > 1:
                yield next_line
                for line in line_broken[1:-1]:
                    yield line
                next_line = line_broken[-1]

    def __init__(self, stream):
        super(IterGzip, self).__init__(IterGzip._scan_chunks(stream))


class JsonLinesReader(FileLikeLineIterable):
    def __init__(self, fileobj, **kwargs):
        self.kwargs = kwargs
        super(JsonLinesReader, self).__init__((json.loads(nl, **kwargs) for nl in fileobj))


def __dict_to_namedtuple(type_name, some_dict):
    tupled = sorted(some_dict.items())
    field_names, field_values = [k for k, _ in tupled], [v for _, v in tupled]
    return namedtuple(type_name, field_names)(*field_values)


COMPRESSION = dict(none=lambda s: s, gzip=IterGzip)
DESERIALIZERS = dict(
    none=lambda s: s,
    json_lines=JsonLinesReader,
    delimited=lambda fobj, dialect='excel', **fmtparams: csv_reader(fobj, dialect=dialect, **fmtparams),
    delimited_as_dict=DictReader,
)
DESERIALIZERS.update(
    csv=DESERIALIZERS['delimited'],
    csv_as_dict=DESERIALIZERS['delimited_as_dict'],
    tsv=lambda fobj, **fmtparams: DESERIALIZERS['delimited'](fobj, dialect=csv_excel_tab, **fmtparams),
    tsv_as_dict=lambda fobj, **fmtparams: DESERIALIZERS['delimited_as_dict'](fobj, dialect=csv_excel_tab, **fmtparams)
)

deserialize = __dict_to_namedtuple('Deserialize', DESERIALIZERS)
compression = __dict_to_namedtuple('Compression', COMPRESSION)
