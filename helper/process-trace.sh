#!/usr/bin/env bash
if [ ! $2 ]; then
	echo Usage: $0 trace-file output-dir
	exit 1
fi
set -e
trace_file=$1
output_dir=$2
output_prefix=$output_dir/$(basename $trace_file)
target_db_size=110000000000
max_num_run_op=500000000
~/tests/helper/twitter-to-plain $output_prefix $target_db_size $max_num_run_op < $trace_file | tee $output_prefix.log
zstdmt $output_prefix-load $output_prefix-run
db_size=$(jq -r ".\"db-size\"" < $output_prefix.json)
if [ $db_size -lt $target_db_size ]; then
	multiple=$((($target_db_size + $db_size - 1) / $db_size))
	~/tests/helper/augment-trace $output_prefix $max_num_run_op $multiple
	prefix=$output_prefix-${multiple}x
	zstdmt $prefix-load $prefix-run
fi
