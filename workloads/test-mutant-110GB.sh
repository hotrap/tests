#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
	exit 1
fi
workload_file=$(realpath -s "$1")
$(dirname $0)/test-mutant-110GB-generic.sh "$2" "" "--enable_fast_generator --workload_file=$workload_file $3"
