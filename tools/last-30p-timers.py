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
run_70p = get_timers('rocksdb-stats-run-70p.txt')
res = []
for i in range(0, len(run)):
    timer = run[i]
    timer_70p = run_70p[i]
    assert timer_70p['name'] == timer['name']
    timer['count'] -= timer_70p['count']
    timer['time(sec)'] -= timer_70p['time(sec)']
    res.append(timer)
print(json5.dumps(res, indent=4, trailing_commas=False))