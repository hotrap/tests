#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

import json5
info = json5.load(open('info.json'))
run_70p_ts = info['run-70%-timestamp(ns)']

hit_rates = common.read_hit_rates('.')
hit_rates = hit_rates[hit_rates['Timestamp(ns)'] > run_70p_ts]
print(hit_rates['hit-rate'].mean())
