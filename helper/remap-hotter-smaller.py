#!/usr/bin/env python3
import sys
import os
import shutil

cnt = {}
for key in sys.stdin:
	key = key.strip()
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
for item in remap.items():
	print(*item)