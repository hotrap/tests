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
	run_start_timestamp=$(hjson-cli -j < info.json | jq -er ".\"run-start-timestamp(ns)\"")
	run_start_progress=$(awk "
		BEGIN {
			res = 0
		}
		{
			if (NR > 1 && \$1 >= $run_start_timestamp) {
				res = \$2;
				exit 0
			}
		}
		END {
			print res
		}
	" progress)
	num_run_op=$(($num_total_op - $run_start_progress))
	progress_70p=$((run_start_progress + $num_run_op * 7 / 10))
	res=$(awk "{
		if (NR > 1 && \$2 >= $progress_70p) {
			print \$1, \$2;
			exit 0
		}
	}" progress)
	timestamp_70p=$(echo $res | cut -sd" " -f1)
	progress_70p=$(echo $res | cut -sd" " -f2)
	num_op=$(($num_total_op - $progress_70p))
fi
echo "$num_op / (($timestamp_100p - $timestamp_70p) / 1000000000)" | bc -l
