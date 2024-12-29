#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
	exit 1
fi
workload_file=$(realpath -s "$1")
$(dirname $0)/test-hotrap-110GB-generic.sh "$2" "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--enable_fast_generator --workload_file=$workload_file $3"
