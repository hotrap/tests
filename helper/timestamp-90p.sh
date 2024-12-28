#!/usr/bin/env sh
num_total_op=$(tail -n1 progress | cut -sd' ' -f2)
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
num_run_op=$((num_total_op - run_start_progress))
progress_90p=$((run_start_progress + num_run_op * 9 / 10))
awk "{
	if (NR > 1 && \$2 >= $progress_90p) {
		print \$1, \$2;
		exit 0
	}
}" progress | cut -sd" " -f1
