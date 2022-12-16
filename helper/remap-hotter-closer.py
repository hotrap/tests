#!/usr/bin/env python3
import sys
from itertools import chain, zip_longest

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
n_unique_keys = len(keys_sorted)
if n_unique_keys == 0:
	exit(0)
pivot = int(n_unique_keys * pivot_ratio)
assert(0 <= pivot and pivot < n_unique_keys)

n1 = min(pivot, n_unique_keys - pivot)
l1 = keys_sorted[pivot-n1:pivot][::-1]
l2 = keys_sorted[pivot:pivot+n1]
# https://stackoverflow.com/questions/7946798/interleave-multiple-lists-of-the-same-length-in-python
def interleave(l1, l2):
    return [x for x in chain.from_iterable(zip_longest(l1, l2)) if x is not None]
keys_closest = interleave(l1, l2)
assert(len(keys_closest) == len(l1) + len(l2))
if pivot > n1:
	assert(pivot + n1 == n_unique_keys)
	p2 = (pivot - n1) // 2
	l1 = keys_sorted[0:p2]
	l2 = keys_sorted[p2:pivot - n1][::-1]
else:
	assert(pivot - n1 == 0)
	base = pivot + n1
	p2 = base + (n_unique_keys - base) // 2
	l1 = keys_sorted[base:p2]
	l2 = keys_sorted[p2:n_unique_keys][::-1]
keys_closest.extend(interleave(l1, l2))
assert(len(keys_closest) == n_unique_keys)

remap = {}
for i in range(0, n_unique_keys):
	remap[keys_sorted_by_cnt[i][0]] = keys_closest[i]
for item in remap.items():
	print(*item)