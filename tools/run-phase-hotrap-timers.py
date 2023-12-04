#!/usr/bin/env python3

import json5
import sys

def get_timers(fname):
    f = open(fname)
    for line in f:
        if line == 'Timers of hotrap\n':
            break
    json_str = ''
    for line in f:
        if line == '],\n':
            json_str += ']'
            break
        json_str += line
    return json5.loads(json_str)

run = get_timers('rocksdb-stats-run.txt')
run_0p = get_timers('rocksdb-stats-load-finish.txt')
res = []
for i in range(0, len(run)):
    timer = run[i]
    timer_0p = run_0p[i]
    assert timer_0p['name'] == timer['name']
    timer['count'] -= timer_0p['count']
    timer['time(sec)'] -= timer_0p['time(sec)']
    res.append(timer)
print(json5.dumps(res, indent=4, trailing_commas=False))