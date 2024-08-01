#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 trace-prefix output-dir [extra-kvexe-args]
	exit 1
fi
trace_file_load=$(realpath $1-load)
trace_file_run=$(realpath $1-run)
$(dirname $0)/test-mutant-110GB-generic.sh "$2" "" "--load=$trace_file_load --run=$trace_file_run --format=plain-length-only $3"
