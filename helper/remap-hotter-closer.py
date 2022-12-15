#!/usr/bin/env python3
import sys
import os
import shutil

if len(sys.argv) != 2:
	print('Usage: ' + sys.argv[0] + ' pivot-ratio')
	exit(1)
pivot_ratio = float(sys.argv[1])
if pivot_ratio < 0 or pivot_ratio > 1:
	print('The pivot ratio must be in the range of [0, 1]')
	exit(1)
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
n = len(keys_sorted)
if n == 0:
	exit(0)
pivot = int(n * pivot_ratio)
assert(0 <= pivot and pivot < n)

n1 = min(pivot, n - pivot)
l1 = keys_sorted[pivot-n1:pivot][::-1]
l2 = keys_sorted[pivot:pivot+n1]
# https://stackoverflow.com/questions/7946798/interleave-multiple-lists-of-the-same-length-in-python
keys_closest = [ val for tup in zip(l1, l2) for val in tup ]
if pivot > n1:
	assert(pivot + n1 == n)
	p2 = (pivot - n1) // 2
	l1 = keys_sorted[0:p2]
	l2 = keys_sorted[p2:pivot - n1][::-1]
else:
	assert(pivot - n1 == 0)
	base = pivot + n1
	p2 = base + (n - base) // 2
	l1 = keys_sorted[base:p2]
	l2 = keys_sorted[p2:n][::-1]
keys_closest.extend([ val for tup in zip(l1, l2) for val in tup ])

remap = {}
for i in range(0, n):
	remap[keys_sorted_by_cnt[i][0]] = keys_closest[i]
for item in remap.items():
	print(*item)