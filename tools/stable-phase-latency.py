#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
from common import *

import pandas as pd

hit_rates = read_hit_rates('.')
warmup_finish_ts = warmup_finish_timestamp(hit_rates)

def work(t):
    latency = pd.read_table(t + '-latency', delim_whitespace=True)
    latency = latency[latency['Timestamp(ns)'] >= warmup_finish_ts].iloc[-1]
    print(latency)
print('Read')
work('read')
print('Insert')
work('insert')
