#!/usr/bin/env python3

import json5
import pandas as pd

info = json5.load(open('info.json'))
run_start_timestamp = info['run-start-timestamp(ns)']
run_end_timestamp = info['run-end-timestamp(ns)']
timers = pd.read_table('timers', delim_whitespace=True)
timers = timers[(run_start_timestamp <= timers['Timestamp(ns)']) & (timers['Timestamp(ns)'] < run_end_timestamp)]

print('Compaction CPU time(s): %f' %((timers.iloc[-1] - timers.iloc[0])['compaction-cpu-micros'] / 1e6))
print('Insert CPU time(s): %f' %((timers.iloc[-1] - timers.iloc[0])['insert-cpu-nanos'] / 1e9))
print('Read CPU time(s): %f' %((timers.iloc[-1] - timers.iloc[0])['read-cpu-nanos'] / 1e9))
