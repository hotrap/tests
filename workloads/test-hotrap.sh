#!/usr/bin/env bash
if [[ $# < 4 || $# > 5 ]]; then
	echo Usage: $0 workload-file output-dir sd-size max-hot-size [switches]
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
workload_file=$(realpath -s "$1")
DIR=$(realpath "$2")
sd_size=$(humanfriendly --parse-size=$3)
max_hot_set_size=$(humanfriendly --parse-size=$4)
if [ $5 ]; then
	switches=$5
else
	switches=0x9
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "$kvexe_dir/rocksdb-kvexe --cleanup --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --switches=$switches --num_threads=8 --max_background_jobs=4 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --export_key_only_trace --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts 2>> $DIR/log.txt"
bash ../helper/hotrap-data.sh "$DIR"
