#!/usr/bin/env sh
if [ $# -lt 3 -o $# -gt 4 ]; then
	echo Usage: $0 version-size trace-prefix output-dir [extra-kvexe-args]
	exit 1
fi
trace_file_load=$(realpath -s "$2-load")
trace_file_run=$(realpath -s "$2-run")
$(dirname $0)/test-$1-generic.sh "$3" "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--load=$trace_file_load --run=$trace_file_run --format=plain-length-only $4"
