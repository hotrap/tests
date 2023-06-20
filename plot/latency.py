#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
latencies = pd.read_table(sys.stdin, names=['operation', 'latency(ns)'], delim_whitespace=True)
res = latencies.groupby(latencies['operation'])['latency(ns)'].apply(list)
insert = np.array(res['INSERT'])
get = np.array(res['GET'])
print('Insert(ns):')
print(np.percentile(insert, [10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9, 99.99]))
print('Get(ns):')
print(np.percentile(get, [10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9, 99.99]))
