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
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --num_threads=16 --max_background_jobs=8 --block_size=16384 --max_bytes_for_level_base=67108864 --level0_file_num_compaction_trigger=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,100000000000}}\" $extra_kvexe_args 2>> log.txt"
bash $workspace/tests/helper/rocksdb-data.sh .
