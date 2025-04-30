#!/usr/bin/env sh
if [ ! "$2" ]; then
	echo Usage: "$0" cluster-id output-dir
	exit 1
fi
set -e
cluster_id=$1
output_dir=$2
mydir=$(realpath "$(dirname $0)")
$mydir/twitter-to-plain.sh $cluster_id $output_dir
cd $output_dir
$mydir/analyze-trace.sh $cluster_id
workload=$cluster_id
if augment=$(jq -er ".augment" < $cluster_id.json); then
	workload=$workload-${augment}x
fi
$mydir/other-stats.sh $workload
