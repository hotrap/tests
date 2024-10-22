#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
mkdir -p $1
DIR=$(realpath "$1")
if [ "$(ls -A $DIR)" ]; then
	echo "$1" is not empty!
	exit 1
fi
prefix="$2"
extra_kvexe_args="$3"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

fd_size=1000000000
max_hot_set_size=500000000
max_ralt_size=33000000

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$prefix $kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_ralt_size=$max_ralt_size --num_threads=16 --max_bytes_for_level_base=67108864 --level0_file_num_compaction_trigger=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --ralt_path=$workspace/testdb/ralt --enable_auto_tuning $extra_kvexe_args 2>> log.txt"
$workspace/tests/helper/hotrap-data.sh .
