#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
mydir=$(dirname "$0")
db_dir="$mydir/../../testdb/db"
"$mydir"/save-common-data.sh "$db_dir" "$1"
mv $db_dir/{rocksdb-stats*.txt,first-level-in-sd,compaction-stats,rand-read-bytes} "$1"
