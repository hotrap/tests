#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload output-dir [switches]
	exit 1
fi
set -e
set -o pipefail
# To make set -e take effect if the output dir does not exists
mkdir -p $2
res="$(ls -A $2)"
if [ "$res" ]; then
	echo "$2" is not empty!
	exit 1
fi
workload="$1"
DIR=$(realpath "$2")
if [ $3 ]; then
	switches=$3
else
	switches=0x3
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --load=$workspace/YCSB-traces/$workload-load --run=$workspace/YCSB-traces/$workload-run --format=plain-length-only --switches=$switches --num_threads=16 --max_background_jobs=8 --block_size=16384 --max_bytes_for_level_base=67108864 --level0_file_num_compaction_trigger=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,100000000000}}\" 2>> log.txt"
bash $workspace/tests/helper/rocksdb-data.sh .
