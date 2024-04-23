#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 output-prefix
	exit 1
fi
set -e
output_prefix=$1

$(dirname $0)/analyze-plain $output_prefix
source $output_prefix
frawk "BEGIN{count=0}{if (\$1 > $db_size * 0.05) {count += 1}}END{print count / NR}" $output_prefix-write-size-since-last-write > $output_prefix-read-with-more-than-5p-write-size
frawk "BEGIN{count=0}{if (\$1 > 512) {count += 1}}END{print count / NR}" $output_prefix-num-reads-since-last-read > $output_prefix-read-with-more-than-512-reads
frawk "BEGIN{count=0}{if (\$1 > 64 * 1024 * 1024) {count += 1}}END{print count / NR}" $output_prefix-read-size-since-last-read > $output_prefix-read-with-more-than-64MiB-read-size
