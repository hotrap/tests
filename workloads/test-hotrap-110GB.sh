#!/usr/bin/env bash
if [[ $# < 4 || $# > 5 ]]; then
	echo Usage: $0 workload-file output-dir max-hot-size max-viscnts-size [extra-kvexe-args]
	exit 1
fi
workload_file=$(realpath -s "$1")
mkdir -p $2
DIR=$(realpath "$2")
if [ "$(ls -A $DIR)" ]; then
	echo "$2" is not empty!
	exit 1
fi
max_hot_set_size=$(humanfriendly --parse-size=$3)
max_viscnts_size=$(humanfriendly --parse-size=$4)
extra_kvexe_args="$5"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

fd_size=10000000000
memtable_size=$((64 * 1024 * 1024))
L1_size=$(($fd_size / 12 / $memtable_size * $memtable_size))

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=0x1 --num_threads=16 --max_background_jobs=8 --block_size=16384 --max_bytes_for_level_base=$L1_size --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts $extra_kvexe_args 2>> log.txt"
bash $workspace/tests/helper/hotrap-data.sh .
