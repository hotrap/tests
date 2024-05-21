#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
from common import *

import pandas as pd

info = json5.load(open(os.path.join('.', 'info.json')))

def work(t):
    latency = pd.read_table(t + '-latency', sep='\s+')
    latency = latency[latency['Timestamp(ns)'] >= info['run-start-timestamp(ns)']].iloc[-1]
    print(latency)
print('Read')
work('read')
print('Insert')
work('insert')
