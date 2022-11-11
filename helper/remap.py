#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' remap-file')
	exit()
remap={}
for line in open(sys.argv[1]):
	s = line.strip().split()
	remap[s[0]] = s[1]
for line in sys.stdin:
	s = line.strip().split()
	if s[2] in remap:
		s[2] = remap[s[2]]
	print(*s)
