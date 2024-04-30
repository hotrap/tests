#!/usr/bin/env bash
if [[ $# < 3 || $# > 4 ]]; then
	echo Usage: $0 trace-file-load trace-file-run output-dir [extra-kvexe-args]
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
extra_kvexe_args="$4"
workspace=$(realpath $(dirname $0)/../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
cd $DIR
$kvexe_dir/rocksdb-kvexe --load --format=plain-length-only --num_threads=16 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=671088640 --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths="{{$workspace/testdb/fd,1000000000000}}" --trace=$trace_file_load $extra_kvexe_args 2>> log.txt
$workspace/tests/helper/exe-while.sh . bash -c "$kvexe_dir/rocksdb-kvexe --run --format=plain-length-only --switches=0x1 --num_threads=16 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=671088640 --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,1000000000000}}\" --trace=$trace_file_run $extra_kvexe_args 2>> log.txt"
bash $workspace/tests/helper/rocksdb-data.sh .
