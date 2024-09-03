#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 2 ]; then
	echo Usage: $0 output-dir [extra-kvexe-args]
	exit 1
fi
mkdir -p $1
res="$(ls -A $1)"
if [ "$res" ]; then
	echo "$1" is not empty!
	exit 1
fi
DIR=$(realpath "$1")
extra_kvexe_args="$2"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

fd_size=1000000000
max_hot_set_size=500000000
max_viscnts_size=33000000

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --num_threads=16 --block_size=16384 --max_bytes_for_level_base=67108864 --level0_file_num_compaction_trigger=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts $extra_kvexe_args 2>> log.txt"
$workspace/tests/helper/hotrap-data.sh .
