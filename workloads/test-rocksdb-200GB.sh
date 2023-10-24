#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload-file output-dir [switches]
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
workload_file=$(realpath $1)
DIR=$(realpath "$2")
if [ $3 ]; then
	switches=$3
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "$kvexe_dir/rocksdb-kvexe --cleanup --switches=$switches --num_threads=8 --max_background_jobs=4 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,50000000000},{$workspace/testdb/cd,1000000000000}}\" 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
