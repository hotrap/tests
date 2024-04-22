#!/usr/bin/env bash
if [ ! $1 ]; then
	echo $0 cluster-id
	exit 1
fi
set -e
cluster_id=$1
if [ -f	$cluster_id.sort.zst ]; then
	unzstd $cluster_id.sort.zst --stdout
	echo Unzipped $cluster_id.sort.zst 1>&2
else
	i=0
	while true; do
		trace_file=$cluster_id.$(printf "%03d" $i)
		if [ ! -f $trace_file.zst ]; then
			break
		fi
		unzstd $trace_file.zst --stdout
		i=$((i+1))
	done
	echo Unzipped $i subtraces 1>&2
fi
