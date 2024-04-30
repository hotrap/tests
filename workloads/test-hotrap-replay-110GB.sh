#!/usr/bin/env bash
if [[ $# < 6 || $# > 7 ]]; then
	echo Usage: $0 trace-file-load trace-file-run output-dir fd-size max-hot-size max-viscnts-size [extra-kvexe-args]
	exit 1
fi
trace_file_load=$(realpath -s "$1")
trace_file_run=$(realpath -s "$2")
mkdir -p $3
DIR=$(realpath "$3")
if [ "$(ls -A $DIR)" ]; then
	echo "$3" is not empty!
	exit 1
fi
fd_size=$(humanfriendly --parse-size=$4)
max_hot_set_size=$(humanfriendly --parse-size=$5)
max_viscnts_size=$(humanfriendly --parse-size=$6)
extra_kvexe_args="$7"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

memtable_size=$((64 * 1024 * 1024))
L1_size=$(($fd_size / 12 / $memtable_size * $memtable_size))

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
time $kvexe_dir/rocksdb-kvexe --load --format=plain-length-only --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --num_threads=16 --max_background_jobs=4 --block_size=16384 --max_bytes_for_level_base=$L1_size --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths="{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}" --viscnts_path=$workspace/testdb/viscnts --trace=$trace_file_load $extra_kvexe_args 2>> log.txt
$workspace/tests/helper/exe-while.sh . bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --run --format=plain-length-only --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=0x1 --num_threads=16 --max_background_jobs=4 --block_size=16384 --max_bytes_for_level_base=$L1_size --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts --trace=$trace_file_run $extra_kvexe_args 2>> log.txt"
bash $workspace/tests/helper/hotrap-data.sh .
