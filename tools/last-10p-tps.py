#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

d = common.VersionData('.')

def calc(iostat):
    iostat = iostat[(iostat['Timestamp(ns)'] >= d.ts_run_90p()) & (iostat['Timestamp(ns)'] <= d.info()['run-end-timestamp(ns)'])]
    return iostat['r/s'].mean()

import pandas as pd
fd = calc(pd.read_table('iostat-fd.txt', sep='\s+'))
print('FD:', fd)
sd = calc(pd.read_table('iostat-sd.txt', sep='\s+'))
print('SD:', sd)
