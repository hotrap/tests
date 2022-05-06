#!/bin/python3

import sys

if __name__ == "__main__":
	cnts = {}
	for line in sys.stdin:
		if line in cnts:
			cnts[line] += 1
		else:
			cnts[line] = 1
	cnt_cnts = {}
	for i in cnts.items():
		cnt = i[1]
		if cnt in cnt_cnts:
			cnt_cnts[cnt] += 1
		else:
			cnt_cnts[cnt] = 1
	cnt_cnts = sorted(cnt_cnts.items())
	print(cnt_cnts)
