#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
mydir=$(dirname "$0")
mydir=$(realpath "$mydir")
output_dir=$(realpath "$1")
cd "$mydir/../../testdb/db"
"$mydir"/save-common-data.sh . "$output_dir"
mv rocksdb-stats*.txt first-level-in-last-tier compaction-stats rand-read-bytes other-stats-load-finish.txt "$output_dir"
