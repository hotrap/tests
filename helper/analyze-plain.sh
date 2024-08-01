#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 2 ]; then
	echo Usage: $0 output-prefix [num-unique-keys]
	exit 1
fi
set -e
output_prefix=$1
mydir=$(dirname $0)

$mydir/analyze-plain $output_prefix --num-unique-keys=$2
db_size=$(jq -er ".\"db-size\"" < $output_prefix.json)

ratio_gt() {
	input=$1
	output=$2
	num=$3
	if [ -s $input ]; then
		frawk "BEGIN{count=0}{if (\$1 > $num) {count += 1}}END{print count / NR}" $input > $output
	else
		echo 0 > $output
	fi
}
ratio_gt $output_prefix-write-size-since-last-write $output_prefix-read-with-more-than-5p-write-size "$db_size * 0.05"
ratio_gt $output_prefix-num-reads-since-last-read $output_prefix-read-with-more-than-512-reads 512
ratio_gt $output_prefix-read-size-since-last-read $output_prefix-read-with-more-than-64MiB-read-size "64 * 1024 * 1024"
