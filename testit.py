
from s3streaming import s3_open, deserialize, compression


spo_b = 's3://prod-prod-spo-datalake/2019/03/17/02/prod-SpoDataLake-1-2019-03-17-02-00-59-8765ddd7-fe41-4fcc-bdc1-0cfefcf8e750'
spo_rds_raw_tsv = 's3://prod-spo-service-data-export/data-export/AdAttribution/AdAttribution-2017011713.tsv'
res_comp_json = 's3://prod-aqueduct-reservoir/SPO/AdImpression/2019/03/14/01/AdAttribution-2019031401.tsv.gz'
zd3_comp_tsv = 's3://zocdoop3/data/test-compression/ad-att-compressed.tsv.gz'

# print(' ')
# print(' ')
# print('s3_open(spo_b, spo_k, deserializer=deserialize.json_lines)')
# f = s3_open(spo_b)
# next_line = next(f)
# print(type(next_line))
# print(next_line)

# print(' ')
# print(' ')
# print('context lib')
# with s3_open(spo_b, deserializer=deserialize.json_lines) as f:
#     print(f)
#     next_line = next(f)
#     print(type(next_line))
#     print(next_line)
#
# print(' ')
# print(' ')
# print('s3_open(spo_b, spo_k, deserializer=deserialize.json_lines)')
# f = s3_open(spo_b, deserializer=deserialize.json_lines)
# next_line = next(f)
# print(type(next_line))
# print(next_line.keys())
#
# print(' ')
# print(' ')
# print('s3_open(spo_rds, raw_tsv, deserializer=deserialize.tsv_as_dict)')
# f = s3_open(spo_rds_raw_tsv, deserializer=deserialize.tsv_as_dict)
# next_line = next(f)
# print(type(next_line))
# print(next_line.keys())
#
#
# print(' ')
# print(' ')
# print('s3_open(spo_rds, raw_tsv, deserializer=deserialize.tsv_as_dict)')
# f = s3_open(spo_rds_raw_tsv, deserializer=deserialize.tsv_as_dict)
# next_line = next(f)
# print(type(next_line))
# print(next_line)


print(' ')
print(' ')
print('s3_open(res, comp_json, deserializer=deserialize.json_lines, compression=compression.gzip)')
with s3_open(res_comp_json, deserializer=deserialize.json_lines, compression=compression.gzip) as f:
    next_line = next(f)
    print(type(next_line))
    print(next_line.keys())
    print(next_line)
    print(len(f.read(2)))


print(' ')
print(' ')
print('s3_open(zd3, comp_tsv, deserializer=deserialize.tsv_as_dict, compression=compression.gzip)')
with s3_open(zd3_comp_tsv, deserializer=deserialize.tsv_as_dict, compression=compression.gzip) as f:
    next_line = next(f)
    print(type(next_line))
    print(next_line.keys())
    print(next_line)


print(' ')
print(' ')
print('s3_open(spo_b, spo_k, deserializer=deserialize.json_lines)')
with s3_open(spo_b, deserializer=deserialize.json_lines) as spo_iter:
    next_spo_iter = next(spo_iter)
    print(type(next_spo_iter))
    print(next_spo_iter)
