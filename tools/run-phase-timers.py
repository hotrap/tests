#!/usr/bin/env python3

import json5
import pandas as pd

info = json5.load(open('info.json'))
run_start_timestamp = info['run-start-timestamp(ns)']
run_end_timestamp = info['run-end-timestamp(ns)']
timers = pd.read_table('timers', sep='\s+')
timers = timers[(run_start_timestamp <= timers['Timestamp(ns)']) & (timers['Timestamp(ns)'] < run_end_timestamp)]
timers = timers.iloc[-1] - timers.iloc[0]

print('Compaction CPU time(s): %f' %(timers['compaction-cpu-micros'] / 1e6))
print('Put CPU time(s): %f' %(timers['put-cpu-nanos'] / 1e9))
print('Get CPU time(s): %f' %(timers['get-cpu-nanos'] / 1e9))
if 'ralt.compaction.cpu.nanos' in timers:
	print('RALT CPU time(s): %f' %((timers['ralt.compaction.cpu.nanos'] + timers['ralt.flush.cpu.nanos'] + timers['ralt.decay.scan.cpu.nanos'] + timers['ralt.decay.write.cpu.nanos']) / 1e9))
if 'ralt.compaction.thread.cpu.nanos' in timers:
	print('RALT threads CPU time(s): %f' %((timers['ralt.compaction.thread.cpu.nanos'] + timers['ralt.flush.thread.cpu.nanos'] + timers['ralt.decay.thread.cpu.nanos']) / 1e9))
