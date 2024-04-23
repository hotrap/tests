#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 dir cluster-id
	exit 1
fi
set -e
dir=$1
cluster_id=$2

trace_prefix=$cluster_id
mkdir -p $dir/stats
cat $dir/$trace_prefix-load $dir/$trace_prefix-run | $(dirname $0)/analyze-plain.sh $dir/stats/$trace_prefix
db_size=$(jq -r ".\"db-size\"" < $dir/$trace_prefix.json)
target_db_size=110000000000
if [ $db_size -lt $target_db_size ]; then
	multiple=$((($target_db_size + $db_size - 1) / $db_size))
	trace_prefix=$trace_prefix-${multiple}x
	cat $dir/$trace_prefix-load $dir/$trace_prefix-run | $(dirname $0)/analyze-plain.sh $dir/stats/$trace_prefix
fi
