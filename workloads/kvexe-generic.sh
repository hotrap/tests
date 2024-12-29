#!/usr/bin/env sh
if [ $# -lt 4 -o $# -gt 5 ]; then
	echo Usage: $0 command cache-size L1-size output-dir [extra-kvexe-args]
	exit 1
fi
command="$1"
cache_size=$(humanfriendly --parse-size="$2")
L1_size=$(humanfriendly --parse-size="$3")
mkdir -p $4
DIR=$(realpath "$4")
if [ "$(ls -A $DIR)" ]; then
    echo "$4" is not empty!
    exit 1
fi
extra_kvexe_args="$5"
cd "$(dirname $0)"
workspace=$(realpath ../..)

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$command \
--switches=0x1 \
--num_threads=16 \
--cache_size=$cache_size \
--max_bytes_for_level_base=$L1_size \
--db_path=$workspace/testdb/db/ \
$extra_kvexe_args 2>> log.txt"
