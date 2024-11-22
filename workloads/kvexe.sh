#!/usr/bin/env sh
if [ $# -lt 5 -o $# -gt 6 ]; then
	echo Usage: $0 command cache-size fd-size L1-size output-dir [extra-kvexe-args]
	exit 1
fi
command="$1"
cache_size=$(humanfriendly --parse-size="$2")
fd_size=$(humanfriendly --parse-size="$3")
L1_size=$(humanfriendly --parse-size="$4")
mkdir -p $5
DIR=$(realpath "$5")
if [ "$(ls -A $DIR)" ]; then
    echo "$5" is not empty!
    exit 1
fi
extra_kvexe_args="$6"
cd "$(dirname $0)"
workspace=$(realpath ../..)

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$command \
--num_threads=16 \
--cache_size=$cache_size \
--max_bytes_for_level_base=$L1_size \
--db_path=$workspace/testdb/db/ \
--db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}}\" \
$extra_kvexe_args 2>> log.txt"
