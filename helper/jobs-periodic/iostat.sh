#!/usr/bin/env bash

echo Timestamp\(ns\) sd_tps sd_kB_read/s sd_kB_wrtn/s cd_tps cd_kB_read/s cd_kB_wrtn/s
while true; do
	# Use bash -c to ensure that "date" is executed for every line
	iostat 1 | awk -f iostat.awk | xargs -I {} bash -c 'echo $(date +%s%N) {}'
done
