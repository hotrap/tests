#!/usr/bin/env bash
if [[ $# < 3 || $# > 4 ]]; then
	echo Usage: $0 trace-file-load trace-file-run output-dir [extra-kvexe-args]
	exit 1
fi
trace_file_load=$(realpath $1)
trace_file_run=$(realpath $2)
$(dirname $0)/test-rocksdb-fd-110GB-generic.sh "$3" "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--load=$trace_file_load --run=$trace_file_run --format=plain-length-only --switches=0x3 $4"
