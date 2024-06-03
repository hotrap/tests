#!/usr/bin/env bash
if [ ! $2 ]; then
	echo Usage: $0 db-dir output-dir
	exit 1
fi
db_dir="$1"
DIR="$2"
mydir=$(realpath $(dirname $0))
testdb_dir=$(realpath -L "$db_dir/..")
du -sh $testdb_dir/db/ $testdb_dir/fd/ $testdb_dir/sd/ >> "$DIR"/log.txt
mv $db_dir/{LOG,latency-*,period_stats,progress,cpu,cputimes,mem,info.json,timers,worker-cpu-nanos} "$DIR"/
if [ -f "$db_dir"/ans-0.xxh64 ]; then
	mv "$db_dir"/ans-*.xxh64 "$DIR"/
fi
if [ -f 0_key_only_trace ]; then
	find "$db_dir" -name "*_key_only_trace" -exec cat {} \; | awk '{if ($1 == "READ" || $1 == "RMW") print $2}' | $mydir/bin/occurrences > "$DIR"/occurrences
fi
"$mydir"/latency-after "$DIR"/
