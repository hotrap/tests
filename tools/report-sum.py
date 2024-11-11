#!/usr/bin/env python3

import pandas as pd

fields = [
    'interval_qps',
    'rocksdb.t0.hit',
    'rocksdb.t1.hit',
    'hotrap.promoted.flush.bytes',
    'hotrap.promoted.2fdlast.bytes',
    'hotrap.promoted.2sdfront.bytes',
    'hotrap.retained.bytes',
    'hotrap.accessed.cold.bytes',
    'hotrap.has_newer_version.bytes',
    'hotrap.scan.hit.t0',
    'hotrap.scan.hit.t1',
]
report = pd.read_table('report.csv', sep=',')
for field in fields:
    if field in report:
        print(field, report[field].sum())
