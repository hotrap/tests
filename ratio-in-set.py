#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' file-of-set')
	exit(1)

path = sys.argv[1]
s = set()
for key in open(path):
	key = key.strip()
	s.add(key)

exists = 0
total = 0
for key in sys.stdin:
	key = key.strip()
	total += 1
	if key in s:
		exists += 1
if total == 0:
	print('0')
else:
	print(exists / total)
