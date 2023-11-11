#!/usr/bin/env python3

import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' dir')
	exit()

import os
import numpy as np

d = sys.argv[1]

first_level_in_cd = int(open(d + '/first-level-in-cd').read())

last_tier0 = 0
last_total = 0
for line in open(d + '/num-accesses'):
    res = line.split(' ')
    timestamp = int(res[0])
    tier0 = 0
    total = 0
    for (level, num_accesses) in enumerate(res[1:]):
        num_accesses = int(num_accesses)
        total += num_accesses
        if level < first_level_in_cd:
            tier0 += num_accesses
    if total - last_total != 0:
        hit_rate = (tier0 - last_tier0) / (total - last_total)
        print("%d %f" %(timestamp, hit_rate))
        last_tier0 = tier0
        last_total = total
