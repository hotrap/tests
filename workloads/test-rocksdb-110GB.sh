#!/usr/bin/env bash
if [[ $# < 3 || $# > 4 ]]; then
	echo Usage: $0 workload-file output-dir fd-size [extra-kvexe-args]
	exit 1
fi
set -e
set -o pipefail
workload_file=$(realpath $1)
mkdir -p $2
DIR=$(realpath "$2")
if [ "$(ls -A $DIR)" ]; then
        echo "$2" is not empty!
        exit 1
fi
fd_size=$(humanfriendly --parse-size=$3)
max_memory=$(humanfriendly --parse-size=1.1GB)
extra_kvexe_args="$4"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "systemd-run --user -E LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 --scope -p MemoryMax=$max_memory $kvexe_dir/rocksdb-kvexe --switches=0x1 --num_threads=16 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=67108864 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}}\" $extra_kvexe_args 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
