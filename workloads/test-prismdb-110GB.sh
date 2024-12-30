#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
	exit 1
fi
workload_file=$(realpath -s "$1")
$(dirname $0)/test-prismdb-110GB-generic.sh "$2" "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--enable_fast_generator --workload_file=$workload_file --sleep_secs_after_load=600 --num_keys=110000000 --stop_upsert_trigger=70000000 $3"
