#!/usr/bin/env sh
if [ $# -lt 4 -o $# -gt 5 ]; then
	echo Usage: $0 command db-path cache-size output-dir [extra-kvexe-args]
	exit 1
fi
command=$1
db_path=$2
cache_size=$(humanfriendly --parse-size="$3")
mkdir -p "$4"
DIR=$(realpath "$4")
if [ "$(ls -A $DIR)" ]; then
    echo "$4" is not empty!
    exit 1
fi
extra_kvexe_args=$5
cd "$(dirname $0)"
workspace=$(realpath ../..)

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
export ASAN_OPTIONS=abort_on_error=1
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$command \
--switches=0x1 \
--num_threads=16 \
--db_path='$db_path' \
--cache_size=$cache_size \
$extra_kvexe_args 2>> log.txt"
