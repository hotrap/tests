#!/usr/bin/env python3

import sys
argc = len(sys.argv)
if argc < 2 or argc > 3:
    print('Usage: ' + sys.argv[0] + ' num-interval [file-path]')
    exit(1)
num_interval = int(sys.argv[1])

import os
if argc == 3:
    last = os.popen('tail -n 1 ' + sys.argv[2]).read().rstrip().split(' ')
    last = [float(v) for v in last]
    def lines():
        for line in open(sys.argv[2]):
            line = line.rstrip().split(' ')
            yield [float(v) for v in line]
    lines = lines()
else:
    line = sys.stdin.readline().rstrip().split(' ')
    n = len(line)
    d = [[float(v) for v in line]]
    for line in sys.stdin:
        line = line.rstrip().split(' ')
        d.append([float(v) for v in line])
    last = d[-1]
    def lines():
        for row in d:
            yield row
    lines = lines()

line = next(lines)
n = len(line)
assert len(last) == n
interval = []
for j in range(0, n):
    interval.append((last[j] - line[j]) / num_interval)
last_sampled = line
print(*last_sampled)
for line in lines:
    assert len(line) == n
    j = 0
    while j < n and line[j] < last_sampled[j] + interval[j]:
        j += 1
    if j == n:
        last_line_sampled = False
        continue
    last_line_sampled = True
    print(*line)
    last_sampled = line
if last_sampled != line:
    print(*line)
