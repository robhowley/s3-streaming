
import json
import gzip
import codecs
from functools import partial
from collections import namedtuple
from csv import (
    DictReader,
    reader as csv_reader,
    excel_tab as csv_excel_tab
)


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


class JsonLinesReader(FileLikeLineIterable):
    def __init__(self, fileobj, **kwargs):
        self.kwargs = kwargs
        super(JsonLinesReader, self).__init__((json.loads(nl, **kwargs) for nl in fileobj))


def __dict_to_namedtuple(type_name, some_dict):
    tupled = sorted(some_dict.items())
    field_names, field_values = [k for k, _ in tupled], [v for _, v in tupled]
    return namedtuple(type_name, field_names)(*field_values)


COMPRESSION = dict(none=lambda s: s, gzip=gzip.open)

DESERIALIZERS = dict(
    none=lambda s: s,
    string=lambda fobj, encoding='utf-8': (s.decode(encoding) for s in fobj),
    json_lines=JsonLinesReader,
    delimited=lambda fobj, dialect='excel', encoding='utf-8', **fmt_kwargs: csv_reader(
        codecs.getreader(encoding)(fobj),
        dialect=dialect,
        **fmt_kwargs
    ),
    delimited_as_dict=lambda fobj, dialect='excel', encoding='utf-8', **fmt_kwargs: DictReader(
        codecs.getreader(encoding)(fobj),
        dialect=dialect,
        **fmt_kwargs
    )
)
DESERIALIZERS.update(
    csv=DESERIALIZERS['delimited'],
    csv_as_dict=DESERIALIZERS['delimited_as_dict'],
    tsv=partial(DESERIALIZERS['delimited'], dialect=csv_excel_tab),
    tsv_as_dict=partial(DESERIALIZERS['delimited_as_dict'], dialect=csv_excel_tab)
)

deserialize = __dict_to_namedtuple('Deserialize', DESERIALIZERS)
compression = __dict_to_namedtuple('Compression', COMPRESSION)
