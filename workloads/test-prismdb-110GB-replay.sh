#!/usr/bin/env sh
if [ ! $2 ]; then
	echo Usage: $0 trace-prefix output-dir
	exit 1
fi
trace_prefix=$1
trace_file_load=$(realpath -s "$trace_prefix-load")
trace_file_run=$(realpath -s "$trace_prefix-run")
mkdir -p $2
DIR=$(realpath "$2")
if [ "$(ls -A $DIR)" ]; then
	echo "$2" is not empty!
	exit 1
fi
fd_size=12179869184
sd_size=1073741824000
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_path=$workspace/kvexe-prismdb/build/rocksdb-kvexe

num_load_op=$(jq -er ".\"num-load-op\"" < $trace_prefix.json)
num_run_inserts=$(jq -er ".\"num-run-inserts\"" < $trace_prefix.json)
num_keys=$(($num_load_op + $num_run_inserts))

max_kvsize_bytes=$(jq -er ".\"load-avg-value-len\"" < $trace_prefix.json)
max_kvsize_bytes=$(($max_kvsize_bytes + 34))

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "$kvexe_path --load=$trace_file_load --run=$trace_file_run --format=plain-length-only --num_threads=16 --cache_size=134217728 --db_path=$workspace/testdb/sd --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,$sd_size}}\" --switches=1 --migrations_logging=1 --read_logging=0 --migration_policy=2 --migration_metric=1 --migration_rand_range_num=8 --migration_rand_range_size=1 --num_keys=$num_keys --optane_threshold=0.1 --slab_dir=$workspace/testdb/fd/slab-%d-%lu-%lu --pop_cache_size=22000000 --read_dominated_threshold=0.95 --stop_upsert_trigger=70000000 --max_kvsize_bytes=$max_kvsize_bytes 2>> log.txt"
$workspace/tests/helper/save-common-data.sh $workspace/testdb/sd "$DIR"
$workspace/tests/helper/last-10p-latency.py .
