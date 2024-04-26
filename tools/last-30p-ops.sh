#!/usr/bin/env bash
set -e
timestamp_100p=$(hjson-cli -j < info.json | jq -er ".\"run-end-timestamp(ns)\"")
num_total_op=$(tail -n1 progress | cut -sd' ' -f2)
if timestamp_70p=$(hjson-cli -j < info.json | jq -er ".\"run-70%-timestamp(ns)\""); then
	if num_load_op=$(hjson-cli -j < info.json | jq -er ".\"num-load-op\""); then
		num_op=$(($num_total_op - $num_load_op))
	else
		num_op=$num_total_op
	fi
	num_op=$(($num_op * 3 / 10))
else
	num_op=$(($num_total_op * 7 / 10))
	res=$(awk "
	{
		if (NR > 1 && \$2 >= $num_op) {
			print \$1, \$2;
			exit 0
		}
	}" < progress)
	timestamp_70p=$(echo $res | cut -sd" " -f1)
	num_op=$(($num_total_op - $(echo $res | cut -sd" " -f2)))
fi
echo "$num_op / (($timestamp_100p - $timestamp_70p) / 1000000000)" | bc -l
