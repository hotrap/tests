#!/usr/bin/env sh
if [ ! $2 ]; then
	echo Usage: $0 db-dir output-dir
	exit 1
fi
mydir=$(dirname "$0")
mydir=$(realpath "$mydir")
DIR=$(realpath "$2")
cd "$1"
mv LOG latency-* period_stats progress cpu cputimes mem info.json timers "$DIR"/
if [ -f worker-cpu-nanos ]; then
	mv worker-cpu-nanos "$DIR"/
fi
if [ -f ans-0.xxh64 ]; then
	mv ans-*.xxh64 "$DIR"/
fi
if [ -f 0_key_only_trace ]; then
	find . -name "*_key_only_trace" -exec cat {} \; | awk '{if ($1 == "READ" || $1 == "RMW") print $2}' | "$mydir"/bin/occurrences > "$DIR"/occurrences
fi
"$mydir"/latency-after "$DIR"/
