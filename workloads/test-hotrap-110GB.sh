#!/usr/bin/env bash
if [[ $# < 5 || $# > 6 ]]; then
	echo Usage: $0 workload-file output-dir sd-size max-hot-size max-viscnts-size [extra-kvexe-args]
	exit 1
fi
mkdir -p $2
res="$(ls -A $2)"
if [ "$res" ]; then
	echo "$2" is not empty!
	exit 1
fi
workload_file=$(realpath -s "$1")
DIR=$(realpath "$2")
sd_size=$(humanfriendly --parse-size=$3)
max_hot_set_size=$(humanfriendly --parse-size=$4)
max_viscnts_size=$(humanfriendly --parse-size=$5)
extra_kvexe_args="$6"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
../helper/exe-while.sh $DIR bash -c "cd $DIR && LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=0x1 --num_threads=16 --max_background_jobs=4 --block_size=16384 --max_bytes_for_level_base=67108864 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts $extra_kvexe_args 2>> log.txt"
bash ../helper/hotrap-data.sh "$DIR"
