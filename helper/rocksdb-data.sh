#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
set -e
DIR=$(realpath "$1")
mydir=$(realpath $(dirname $0))
cd $mydir
cd ../../testdb
du -sh db/ sd/ cd/ >> "$DIR"/log.txt
cd db
mv LOG rocksdb-stats*.txt progress cpu mem "$DIR"/
if [ -f key_only_trace_0 ]; then
	find . -name "key_only_trace_*" -exec cat {} \; | awk '{if ($1 == "READ") print $2}' | $mydir/bin/occurrences > occurrences
fi
$mydir/latency-percentile . "$DIR"/
if [ -f ans_0 ]; then
	sha256sum ans_* > "$DIR"/ans.sha256
fi
