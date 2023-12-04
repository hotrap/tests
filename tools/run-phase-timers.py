#!/usr/bin/env python3

import json5
import pandas as pd

info = json5.load(open('info.json'))
run_start_timestamp = info['run-start-timestamp(ns)']
run_end_timestamp = info['run-end-timestamp(ns)']
timers = pd.read_table('timers', delim_whitespace=True)
timers = timers[(run_start_timestamp <= timers['Timestamp(ns)']) & (timers['Timestamp(ns)'] < run_end_timestamp)]
compaction_cpu_time_secs = (timers.iloc[-1] - timers.iloc[0])['compaction-cpu-micros'] / 1e6
print('Compaction CPU time(s): %f' %compaction_cpu_time_secs)
