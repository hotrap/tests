#!/usr/bin/env sh
if [ ! $2 ]; then
	echo Usage: $0 cluster-id output-dir
	exit 1
fi
set -e
cluster_id=$1
output_dir=$2
target_db_size=110000000000
max_num_run_op=500000000

mydir=$(dirname $0)
output_prefix=$output_dir/$cluster_id
$mydir/unzstd-trace.sh $cluster_id | /bin/time $mydir/twitter-to-plain $output_prefix $target_db_size $max_num_run_op 2>&1 | tee $output_prefix.log
if augment=$(jq -er ".augment" < $output_prefix.json); then
	output_prefix=$output_prefix-${augment}x
fi
zstdmt --no-progress $output_prefix-load $output_prefix-run
