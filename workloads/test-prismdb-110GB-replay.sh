#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 trace-prefix output-dir [extra-kvexe-args]
	exit 1
fi
trace_prefix=$1
trace_file_load=$(realpath -s "$trace_prefix-load")
trace_file_run=$(realpath -s "$trace_prefix-run")

num_load_op=$(jq -er ".\"num-load-op\"" < $trace_prefix.json)
num_run_inserts=$(jq -er ".\"num-run-inserts\"" < $trace_prefix.json)
num_keys=$(($num_load_op + $num_run_inserts))

max_kvsize_bytes=$(jq -er ".\"load-avg-value-len\"" < $trace_prefix.json)
max_kvsize_bytes=$(($max_kvsize_bytes + 34))

num_reads=$(jq -er ".\"num-reads\"" < $trace_prefix.json)
stop_upsert_trigger=$(($num_reads / 10 * 7))

$(dirname $0)/test-prismdb-110GB-generic.sh "$2" "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--load=$trace_file_load --run=$trace_file_run --format=plain-length-only --num_keys=$num_keys --stop_upsert_trigger=$stop_upsert_trigger --max_kvsize_bytes=$max_kvsize_bytes $3"
