#!/usr/bin/env python3
import sys

cnt = {}
for key in sys.stdin:
	key = key.strip()
	if key in cnt:
		cnt[key] += 1
	else:
		cnt[key] = 1

cnt_key = {}
for item in cnt.items():
	if item[1] in cnt_key:
		cnt_key[item[1]].append(item[0])
	else:
		cnt_key[item[1]] = [item[0]]
cnt_key = sorted(cnt_key.items())

keys_sorted = sorted(cnt)
remap = {}
cur_keys = set()
waiting = []
for key in keys_sorted:
	if len(cur_keys) == len(waiting):
		for (k, v) in zip(cur_keys, waiting):
			remap[k] = v
		cur_keys = set(cnt_key.pop()[1])
		assert(len(cur_keys) != 0)
		waiting = []
	if key in cur_keys:
		cur_keys.discard(key)
		# Do not remap
	else:
		waiting.append(key)
assert(len(cnt_key) == 0)
assert(len(cur_keys) == len(waiting))
for (k, v) in zip(cur_keys, waiting):
	remap[k] = v

for item in remap.items():
	print(*item)