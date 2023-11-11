#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
import pandas as pd
import numpy as np

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)

d = sys.argv[1]

quantiles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.999, 0.9999]
types = ['read', 'insert', 'update', 'rmw']
for t in types:
    path = os.path.join(d, t + '-latency-cdf')
    if not os.path.exists(path):
        continue
    f = open(os.path.join(d, t + '-latency'), 'w')
    cdf = pd.read_table(path, delim_whitespace=True, names=['latency', 'cdf'])
    latencies = np.array(cdf['latency'])
    cdf = np.array(cdf['cdf'])
    proportion = np.concatenate(([cdf[0]], (cdf[1:] - cdf[:-1])))
    average = (latencies * proportion).sum()
    max_latency = latencies[-1]
    print('Average %f' %average, file=f)
    print('Max %d' %max_latency, file=f)
    for quantile in quantiles:
        print('%g %d' %(quantile, latencies[np.searchsorted(cdf, quantile)]), file=f)
