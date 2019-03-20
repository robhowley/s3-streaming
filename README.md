[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# s3-streaming: handling S3 objects like regular files
Storing, retrieving and using files in S3 is a big deal so it should be easy. It should also ...
* stream the data
* have an api that is python file-io like
* handle some of the desearization and compression stuff because why not
 
## Install

```bash
pip install s3-streaming
```

## Streaming S3 objects like regular files

### The basics
Opening and reading S3 objects is similar to regular python io. The only difference is that you need to provide a 
`boto3.session.Session` instance to handle the bucket access. 

```python
import boto3
from s3streaming import s3_open


with s3_open('s3://bucket/key', boto_session=boto3.session.Session()) as f:
    for next_line in f:
        print(next_line)
```

### Injecting deserialization and compression handling in stream
Consider a file that is `gzip` compressed and contains lines of `json`. There's some boilerplate in dealing with that,
but why bother? Just handle that in stream.

```python
from s3streaming import s3_open, deserialize, compression


reader_settings = dict(
  boto_session=boto3.session.Session(),
  deserializer=deserialize.json_lines, 
  compression=compression.gzip
)

with s3_open('s3://bucket/key.gzip', **reader_settings) as f:
    for next_line in f:
        print(next_line.keys())    # because the file was decompressed ...
        print(next_line.values())  #   ... and the json is a dict!

```

Other `deserialize` options include 
* `csv`
* `csv_as_dict`
* `tsv`
* `tsv_as_dict`
