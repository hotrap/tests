#!/usr/bin/env python3
import sys
from dataclasses import dataclass
from itertools import chain, zip_longest
import random

if len(sys.argv) == 1:
	print('Usage: ' + sys.argv[0] + ' pivot-ratios')
	exit(1)
num = len(sys.argv) - 1
pivot_ratios = []
for i in range(0, num):
	pivot_ratios.append(float(sys.argv[i + 1]))
keys = []
for key in sys.stdin:
	key = key.strip()
	keys.append(key)
nkeys = len(keys)
base = nkeys // num
mod = nkeys % num
lens = [base] * (num - mod) + [base + 1] * mod
segments = []
cur = 0
for i in range(0, num):
	segments.append(keys[cur:cur + lens[i]])
	cur += lens[i]

counter_key_segments: dict[int, dict[str, list[int]]] = {}
for i in range(0, num):
	cnt: dict[str, int] = {}
	for key in segments[i]:
		if key in cnt:
			cnt[key] += 1
		else:
			cnt[key] = 1
	for (key, counter) in cnt.items():
		if counter not in counter_key_segments:
			counter_key_segments[counter] = {}
		if key in counter_key_segments[counter]:
			counter_key_segments[counter][key].append(i)
		else:
			counter_key_segments[counter][key] = [i]
	segments[i] = sorted(cnt)

# https://stackoverflow.com/questions/7946798/interleave-multiple-lists-of-the-same-length-in-python
def interleave(l1, l2):
    return [x for x in chain.from_iterable(zip_longest(l1, l2)) if x is not None]
def rearrange_by_pivot(keys_sorted, ratio):
	pivot = int(len(segments[i]) * ratio)
	n = len(segments[i])
	n1 = min(pivot, n - pivot)
	l1 = keys_sorted[pivot-n1:pivot][::-1]
	l2 = keys_sorted[pivot:pivot+n1]
	keys_closest = interleave(l1, l2)
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
	keys_closest.extend(interleave(l1, l2))
	assert(len(keys_closest) == len(keys_sorted))
	return keys_closest
for i in range(0, num):
	segments[i] = rearrange_by_pivot(segments[i], pivot_ratios[i])

keys_mapped_from: set[str] = set()
keys_mapped_to: set[str] = set()
remap = {}
remain_mapped_from = []
def take_key(keys: list[str], cursor: int):
	while True:
		if cursor == len(keys):
			return (cursor, None)
		key = keys[cursor]
		cursor += 1
		if key not in keys_mapped_to:
			return (cursor, key)
def remap_in_segment(keys: list[str], cursor: int, mapped_from: set[str]):
	mapped_to = []
	while len(mapped_from) > len(mapped_to):
		(cursor, key) = take_key(keys, cursor)
		if key is None:
			while len(mapped_from) > len(mapped_to):
				remain_mapped_from.append(mapped_from.pop())
			break
		if key in mapped_from:
			# Map to itself, no need to remap
			mapped_from.discard(key)
			assert(key not in keys_mapped_from)
			assert(key not in keys_mapped_to)
			keys_mapped_from.add(key)
			keys_mapped_to.add(key)
		else:
			mapped_to.append(key)
	assert(len(mapped_from) == len(mapped_to))
	for (k, v) in zip(mapped_from, mapped_to):
		assert(k not in remap)
		assert(k not in keys_mapped_from)
		assert(v not in keys_mapped_to)
		remap[k] = v
		keys_mapped_from.add(k)
		keys_mapped_to.add(v)
	return cursor

cursors = [0] * num
counter_key_segments = sorted(counter_key_segments.items(), reverse=True)
for (_, key_segments) in counter_key_segments:
	mapped_from: dict[int, list[str]] = {}
	for (key, ids) in key_segments.items():
		if key in keys_mapped_from:
			continue
		# TODO: A better way?
		id = ids[random.randrange(0, len(ids))]
		if id in mapped_from:
			mapped_from[id].append(key)
		else:
			mapped_from[id] = [key]
	mapped_from = list(mapped_from.items())
	random.shuffle(mapped_from)
	for (id, keys) in mapped_from:
		# print(id, file=sys.stderr)
		cursors[id] = remap_in_segment(segments[id], cursors[id], set(keys))

for i in range(0, num):
	for key in segments[i][cursors[i]:]:
		if key in keys_mapped_to:
			continue
		while True:
			assert(len(remain_mapped_from) > 0)
			k = remain_mapped_from.pop()
			if k not in keys_mapped_from:
				break
		assert(k not in remap)
		assert(k not in keys_mapped_from)
		assert(key not in keys_mapped_to)
		remap[k] = key
		keys_mapped_from.add(k)
		keys_mapped_to.add(key)
assert(len(remain_mapped_from) == 0)

# Sanity check
assert(len(keys_mapped_from) == len(keys_mapped_to))
assert(len(keys_mapped_from) >= len(remap))
for key in keys_mapped_from:
	assert(key in keys_mapped_to)
keys_mapped_from = set()
keys_mapped_to = set()
for item in remap.items():
	assert(item[0] != item[1])
	assert(item[0] not in keys_mapped_from)
	keys_mapped_from.add(item[0])
	assert(item[1] not in keys_mapped_to)
	keys_mapped_to.add(item[1])
for key in keys_mapped_from:
	assert(key in keys_mapped_to)

for item in remap.items():
	print(*item)