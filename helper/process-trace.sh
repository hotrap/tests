#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 output-prefix
	exit 1
fi
set -e
output_prefix=$1
target_db_size=110000000000
max_num_run_op=500000000
/bin/time $(dirname $0)/twitter-to-plain $output_prefix $target_db_size $max_num_run_op |& tee $output_prefix.log
zstdmt $output_prefix-load $output_prefix-run
db_size=$(jq -r ".\"db-size\"" < $output_prefix.json)
if [ $db_size -lt $target_db_size ]; then
	multiple=$((($target_db_size + $db_size - 1) / $db_size))
	$(dirname $0)/augment-trace $output_prefix $max_num_run_op $multiple
	prefix=$output_prefix-${multiple}x
	zstdmt $prefix-load $prefix-run
fi
