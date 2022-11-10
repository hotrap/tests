#!/usr/bin/env python3
import sys
import os
import shutil

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' trace-file')
	exit()
# Assume that the trace is clean
trace_file_path = sys.argv[1]
cnt = {}
for line in open(trace_file_path):
	s = line.split()
	if s[0] == 'READ':
		key = s[2]
		if key in cnt:
			cnt[key] += 1
		else:
			cnt[key] = 1
keys_sorted = sorted(cnt)
keys_sorted_by_cnt = sorted(cnt.items(), key = lambda item: item[1], reverse=True)
assert(len(keys_sorted) == len(keys_sorted_by_cnt))
remap = {}
for i in range(0, len(keys_sorted_by_cnt)):
	remap[keys_sorted_by_cnt[i][0]] = keys_sorted[i]
for line in open(trace_file_path):
	s = line.strip().split()
	if s[2] in remap:
		s[2] = remap[s[2]]
	print(*s)