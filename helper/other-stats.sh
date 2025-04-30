#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: "$0" trace-prefix
	exit
fi
set -e
mydir=$(dirname $0)
. $mydir/modules/sorted_occurrence_cdf.sh

trace_prefix=$1

stat_cdf_sample() {
	stat_name=$1
	if [ ! -s stats/$trace_prefix-$stat_name ]; then
		touch stats/$trace_prefix-$stat_name-cdf-sampled-100
		return
	fi
	sort -n stats/$trace_prefix-$stat_name | sorted_occurrence_cdf > stats/$trace_prefix-$stat_name-cdf
	"$mydir"/sample.py 100 stats/$trace_prefix-$stat_name-cdf > stats/$trace_prefix-$stat_name-cdf-sampled-100
}

stat_cdf_sample write-size-since-last-write
stat_cdf_sample num-reads-since-last-read
stat_cdf_sample read-size-since-last-read
