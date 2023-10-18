#!/usr/bin/env bash
if [[ $# < 3 || $# > 5 ]]; then
	echo Usage: $0 sd-size workload-file output-dir [num-threads] [switches]
	exit 1
fi
set -e
set -o pipefail
# To make set -e take effect if the output dir does not exists
mkdir -p $3
res="$(ls -A $3)"
if [ "$res" ]; then
        echo "$3" is not empty!
        exit 1
fi
sd_size=$(humanfriendly --parse-size=$1)
workload_file=$(realpath $2)
DIR=$(realpath "$3")
if [ $4 ]; then
	num_threads=$4
else
	num_threads=1
fi
if [ $5 ]; then
	switches=$5
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "$kvexe_dir/rocksdb-kvexe --cleanup --switches=$switches --num_threads=$num_threads --max_background_jobs=4 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,100000000000}}\" 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
