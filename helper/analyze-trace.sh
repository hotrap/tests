#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 cluster-id
	exit 1
fi
set -e
mydir=$(dirname $0)
cluster_id=$1
. $mydir/modules/hotspot_op.sh

trace_prefix=$cluster_id
if augment=$(jq -er ".augment" < $trace_prefix.json); then
	trace_prefix=$trace_prefix-${augment}x
fi
num_unique_keys=$(jq -er ".\"num-unique-keys\"" < $trace_prefix.json)
mkdir -p stats
cat $trace_prefix-load $trace_prefix-run | $(dirname $0)/analyze-plain.sh stats/$trace_prefix $num_unique_keys

frawk '{if ($1 == "READ") print $2;}' $trace_prefix-run | huniq -cS | frawk 'BEGIN{sum=0}{sum += $1; print NR, sum}' > stats/$trace_prefix-read-cdf
if [ -s stats/$trace_prefix-read-cdf ]; then
	hotspot_op stats/$trace_prefix-read-cdf > stats/$trace_prefix-read-hot-5p-read
else
	echo 0 > stats/$trace_prefix-read-hot-5p-read
fi
