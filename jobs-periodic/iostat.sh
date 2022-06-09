#!/usr/bin/env bash

# timestamp(ns) tps kB_read/s kB_wrtn/s
while true; do
	# Use bash -c to ensure that "date" is executed for every line
	iostat 1 | awk -f iostat.awk | xargs -I {} bash -c 'echo $(date +%s%N) {}'
done
