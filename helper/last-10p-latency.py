#!/usr/bin/env python3

import sys
if len(sys.argv) != 2:
    print('Usage: ' + sys.argv[0] + ' data-dir')
    exit(1)
data_dir = sys.argv[1]

import os
import pandas as pd
import numpy as np

i = 0
latencies = []
while True:
    try:
        f = open(os.path.join(data_dir, 'latency-' + str(i)))
    except FileNotFoundError:
        break
    i += 1
    latency = pd.read_table(f, names=['type', 'latency(ns)'], sep='\s+')
    latency = latency.iloc[len(latency) - len(latency) // 10:]
    latency = latency.groupby('type')['latency(ns)'].apply(list)['READ']
    latencies.append(latency)
print(str(i) + ' latency files processsed')
latency = np.array([ elem for latency in latencies for elem in latency])
percentiles = [50, 99, 99.9]
values = np.percentile(latency, percentiles)
f = open(os.path.join(data_dir, 'last-10p-read-latency'), mode='w')
print('Average', file=f, end='')
for percentile in percentiles:
    print(' ' + str(percentile) + '%', file=f, end='')
print(file=f)
print(latency.mean(), file=f, end='')
for value in values:
    print(' %f' %value, file=f, end='')
print(file=f)
