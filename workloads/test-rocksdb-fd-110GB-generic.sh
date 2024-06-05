#!/usr/bin/env bash
if [[ $# < 1 || $# > 3 ]]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
mkdir -p $1
res="$(ls -A $1)"
if [ "$res" ]; then
	echo "$1" is not empty!
    exit 1
fi
DIR=$(realpath "$1")
prefix="$2"
extra_kvexe_args="$3"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "$prefix $kvexe_dir/rocksdb-kvexe --switches=0x1 --num_threads=16 --max_background_jobs=8 --block_size=16384 --cache_size=134217728 --max_bytes_for_level_base=671088640 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,1000000000000}}\" $extra_kvexe_args 2>> log.txt"
bash $workspace/tests/helper/rocksdb-data.sh .
