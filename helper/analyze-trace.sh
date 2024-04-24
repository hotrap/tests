#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 cluster-id
	exit 1
fi
set -e
cluster_id=$1

trace_prefix=$cluster_id
augment=$(jq -er ".augment" < $trace_prefix.json)
if [ $? -eq 0 ]; then
	trace_prefix=$trace_prefix-${augment}x
fi
mkdir -p stats
cat $trace_prefix-load $trace_prefix-run | $(dirname $0)/analyze-plain.sh stats/$trace_prefix
