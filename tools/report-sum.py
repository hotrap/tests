#!/usr/bin/env python3

import pandas as pd

fields = [
    'hotrap.promoted.flush.bytes',
    'hotrap.promoted.2fdlast.bytes',
    'hotrap.promoted.2sdfront.bytes',
    'hotrap.retained.bytes',
    'hotrap.accessed.cold.bytes',
    'hotrap.has_newer_version.bytes',
]
report = pd.read_table('report.csv', sep=',')
for field in fields:
    print(field, report[field].sum())
