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
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$prefix $kvexe_dir/rocksdb-kvexe --num_threads=16 --block_size=16384 --cache_size=201326592 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,1000000000000}}\" $extra_kvexe_args 2>> log.txt"
$workspace/tests/helper/rocksdb-data.sh .
