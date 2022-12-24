#!/usr/bin/env python3
import sys
import random
import string
import math

if len(sys.argv) != 5:
	print('Usage: ' + sys.argv[0] + ' num-operations num-workset hot-ratio read-ratio')
	exit(1)

n = int(sys.argv[1])
num_workset = int(sys.argv[2])
hot_ratio = float(sys.argv[3])
read_ratio = float(sys.argv[4])
workset_op = n // num_workset

workset_digits = int(math.ceil(math.log10(workset_op))) + 1
workset_size = int(10 ** workset_digits)
id_digits = int(math.ceil(math.log10(num_workset)))
key_format = '{:0' + str(id_digits) + 'd}_{:0' + str(workset_digits) + 'd}'

def insert():
	while True:
		offset = random.randrange(0, workset_size)
		key = key_format.format(id, offset)
		if key not in keys_set:
			break
	keys_set.add(key)
	if random.uniform(0, 1) < hot_ratio:
		keys_array.append(key)
	value = ''.join(random.choices(string.ascii_letters + string.digits, k=1000))
	print('INSERT ' + key + ' ' + value)

for id in range(0, num_workset):
	keys_set = set()
	keys_array = []
	remain = workset_op
	while remain != 0 and len(keys_array) == 0:
		insert()
		remain -= 1
	while remain != 0:
		remain -= 1
		if random.uniform(0, 1) < read_ratio:
			print('READ ' + keys_array[random.randrange(0, len(keys_array))])
		else:
			insert()