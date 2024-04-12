#!/usr/bin/env bash
if [[ $# < 3 || $# > 4 ]]; then
	echo Usage: $0 trace-file-load trace-file-run output-dir [switches]
	exit 1
fi
set -e
set -o pipefail
trace_file_load=$(realpath $1)
trace_file_run=$(realpath $2)
mkdir -p $3
DIR=$(realpath "$3")
if [ "$(ls -A $DIR)" ]; then
        echo "$3" is not empty!
        exit 1
fi
if [ $4 ]; then
	switches=$4
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-secondary-cache/build/

ulimit -n 100000
$kvexe_dir/rocksdb-kvexe --load --format=plain-length-only --switches=$switches --num_threads=16 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=335544320 --secondary_cache_size=6000000000 --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths="{{$workspace/testdb/fd,4030000000},{$workspace/testdb/sd,1000000000000}}" --trace=$trace_file_load 2>> $DIR/log.txt
../helper/exe-while.sh $DIR bash -c "$kvexe_dir/rocksdb-kvexe --run --format=plain-length-only --switches=$switches --num_threads=16 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=335544320 --secondary_cache_size=6000000000 --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,4030000000},{$workspace/testdb/sd,1000000000000}}\" --trace=$trace_file_run 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
