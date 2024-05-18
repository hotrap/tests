#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload-file output-dir [switches]
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
if [ $3 ]; then
	switches=$3
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-secondary-cache/build/
fd_size=4030000000

memtable_size=$((64 * 1024 * 1024))
L1_size=$(($fd_size / 12 / $memtable_size * $memtable_size))

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_dir/rocksdb-kvexe --switches=$switches --num_threads=16 --max_background_jobs=8 --block_size=16384 --cache_size=134217728 --max_bytes_for_level_base=$L1_size --secondary_cache_size=6000000000 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}}\" 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
