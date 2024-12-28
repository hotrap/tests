#!/usr/bin/env sh
if [ ! $2 ]; then
	echo Usage: $0 workload-file output-dir
	exit 1
fi
mkdir -p $2
res="$(ls -A $2)"
if [ "$res" ]; then
	echo "$2" is not empty!
	exit 1
fi
workload_file=$(realpath -s "$1")
DIR=$(realpath "$2")
fd_size=12179869184
sd_size=1073741824000
cd "$(dirname $0)"
workspace=$(realpath ../..)

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$workspace/kvexe-rocksdb/build/rocksdb-kvexe --sleep_secs_after_load=600 --num_threads=16 --cache_size=335544320 --format=ycsb --db_path=$workspace/testdb/sd --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,$sd_size}}\" --switches=1 --migrations_logging=1 --read_logging=0 --migration_policy=2 --migration_metric=1 --migration_rand_range_num=8 --migration_rand_range_size=1 --num_keys=110000000 --optane_threshold=0.1 --slab_dir=$workspace/testdb/fd/slab-%d-%lu-%lu --pop_cache_size=22000000 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --read_dominated_threshold=0.95 --stop_upsert_trigger=70000000 2> log.txt"
$workspace/tests/helper/save-common-data.sh $workspace/testdb/sd "$DIR"
$workspace/tests/helper/last-10p-latency.py "$DIR"
