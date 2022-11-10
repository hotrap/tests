#!/usr/bin/env python3

import sys

for line in sys.stdin:
	line = line.strip()
	op = line.split()[0]
	if op == 'READ' or op == 'INSERT' or op == 'UPDATE':
		print(line)
	else:
		print("Ignore line: %s" %line, file=sys.stderr)
