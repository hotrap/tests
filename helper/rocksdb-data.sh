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
mv LOG rocksdb-stats*.txt progress cpu mem info.json "$DIR"/
if [ -f 0_key_only_trace_70_100 ]; then
	find . -name "*_key_only_trace_70_100" -exec cat {} \; | awk '{if ($1 == "READ" || $1 == "RMW") print $2}' | $mydir/bin/occurrences > occurrences
fi
$mydir/latency-percentile . "$DIR"/
if [ -f ans_0 ]; then
	sha256sum ans_* > "$DIR"/ans.sha256
fi
