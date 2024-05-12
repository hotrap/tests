#!/usr/bin/env bash
if [[ $# < 4 || $# > 5 ]]; then
	echo Usage: $0 trace-file-load trace-file-run output-dir fd-size [extra-kvexe-args]
	exit 1
fi
set -e
set -o pipefail
trace_file_load=$(realpath $1)
trace_file_run=$(realpath $2)
mkdir -p $3
DIR=$(realpath "$3")
if [ "$(ls -A $DIR)" ]; then
	echo "$3" is not empty!
	exit 1
fi
fd_size=$(humanfriendly --parse-size=$4)
extra_kvexe_args="$5"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

memtable_size=$((64 * 1024 * 1024))
L1_size=$(($fd_size / 12 / $memtable_size * $memtable_size))

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "$kvexe_dir/rocksdb-kvexe --load=$trace_file_load --run=$trace_file_run --format=plain-length-only --switches=0x1 --num_threads=16 --max_background_jobs=8 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=$L1_size --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}}\" $extra_kvexe_args 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
