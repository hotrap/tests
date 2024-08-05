#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(sys.argv[0]), '../helper/'))
import common

d = common.VersionData('.')
hit_rates = common.read_hit_rates('.')
hit_rates = hit_rates[hit_rates['Timestamp(ns)'] > d.ts_run_90p()]
print(hit_rates['hit-rate'].mean())
