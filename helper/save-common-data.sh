#!/usr/bin/env sh
if [ ! $2 ]; then
	echo Usage: $0 db-dir output-dir
	exit 1
fi
mydir=$(dirname "$0")
mydir=$(realpath "$mydir")
DIR=$(realpath "$2")
cd "$1"
"$mydir"/latency-after .
mv LOG *-latency period_stats progress cpu cputimes mem info.json timers run-phase-perf-context-* run-phase-iostats-contexts-* "$DIR"/
mv_if_exists() {
	if [ -f "$1" ]; then
		mv "$1" "$DIR"/
	fi
}
mv_if_exists worker-cpu-nanos
mv_if_exists report.csv
if [ -f ans-0.xxh64 ]; then
	mv ans-*.xxh64 "$DIR"/
fi
if [ -f 0_key_only_trace ]; then
	find . -name "*_key_only_trace" -exec cat {} \; | awk '{if ($1 == "READ" || $1 == "RMW") print $2}' | "$mydir"/bin/occurrences > "$DIR"/occurrences
fi
