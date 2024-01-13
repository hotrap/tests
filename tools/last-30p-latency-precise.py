#!/usr/bin/env python3

import os
import json5
import numpy as np
import pandas as pd

info = json5.load(open('info.json'))
run_70p_ts = info['run-70%-timestamp(ns)']

read_latencies = []
insert_latencies = []
i = 0
while True:
    path = 'latency-' + str(i)
    if not os.path.exists(path):
        break
    latency = pd.read_table(path, delim_whitespace=True, names=['Timestamp(ns)', 'type', 'latency'])
    latency = latency[latency['Timestamp(ns)'] >= run_70p_ts]
    latency = latency.groupby('type')['latency'].apply(list)
    if 'READ' in latency:
        read_latencies.append(latency['READ'])
    if 'INSERT' in latency:
        insert_latencies.append(latency['INSERT'])
    i += 1
def work(latencies):
    latencies = np.array([x for array in latencies for x in array])
    print('Average %f ns' %(latencies.mean()))
    percentiles = [10, 20, 30, 40, 50, 60, 70, 80, 90, 99, 99.9]
    a = np.percentile(latencies, percentiles)
    for i in range(0, len(a)):
        print('%f%% %f ns' %(percentiles[i], a[i]))
print('Read')
work(read_latencies)
if len(insert_latencies) != 0:
    print('Insert')
    work(insert_latencies)
