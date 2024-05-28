#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload output-dir [switches]
	exit 1
fi
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
kvexe_dir=$workspace/kvexe/build/

fd_size=1000000000
max_hot_set_size=500000000
max_viscnts_size=33000000

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --load=$workspace/YCSB-traces/$workload-load --run=$workspace/YCSB-traces/$workload-run --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=$switches --num_threads=16 --max_background_jobs=8 --block_size=16384 --max_bytes_for_level_base=67108864 --level0_file_num_compaction_trigger=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts 2>> log.txt"
bash $workspace/tests/helper/hotrap-data.sh .
