#!/usr/bin/env bash
if [[ $# < 4 || $# > 6 ]]; then
	echo Usage: $0 workload-file output-dir fd-size max-hot-size max-viscnts-size [switches]
	exit 1
fi
mkdir -p $2
res="$(ls -A $2)"
if [ "$res" ]; then
	echo "$2" is not empty!
	exit 1
fi
workload_file=$(realpath "$1")
DIR=$(realpath "$2")
fd_size=$(humanfriendly --parse-size=$3)
max_hot_set_size=$(humanfriendly --parse-size=$4)
max_viscnts_size=$(humanfriendly --parse-size=$5)
if [ $6 ]; then
	switches=$6
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
../helper/exe-while.sh $DIR bash -c "cd $DIR && LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=$switches --num_threads=16 --max_background_jobs=4 --block_size=16384 --max_bytes_for_level_base=67108864 --level0_file_num_compaction_trigger=1 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts 2>> log.txt"
bash ../helper/hotrap-data.sh "$DIR"
