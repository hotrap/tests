#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
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
extra_kvexe_args="$3"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --switches=0x1 --num_threads=16 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=67108864 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,1000000000000}}\" extra_kvexe_args 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
