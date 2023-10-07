#!/usr/bin/env bash
if [[ $# < 4 || $# > 6 ]]; then
	echo Usage: $0 sd-size max-hot-size workload-file output-dir [num-threads] [switches]
	exit 1
fi
set -e
set -o pipefail
# To make set -e take effect if the output dir does not exists
mkdir -p $4
res="$(ls -A $4)"
if [ "$res" ]; then
	echo "$4" is not empty!
	exit 1
fi
sd_size=$(humanfriendly --parse-size=$1)
max_hot_set_size=$(humanfriendly --parse-size=$2)
workload_file=$(realpath "$3")
DIR=$(realpath "$4")
if [ $5 ]; then
	num_threads=$5
else
	num_threads=1
fi
if [ $6 ]; then
	switches=$6
else
	switches=0x9
fi
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

ulimit -n 100000
tmp_dir=$(mktemp -d)
../helper/exe-while.sh $tmp_dir bash -c "$kvexe_dir/rocksdb-kvexe --cleanup --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --switches=$switches --num_threads=$num_threads --max_background_jobs=4 --level0_file_num_compaction_trigger=1 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --export_key_only_trace --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts 2>> $4/log.txt"
mv -n $tmp_dir/* $4/
rm -r $tmp_dir
bash ../helper/hotrap-data.sh "$DIR"
