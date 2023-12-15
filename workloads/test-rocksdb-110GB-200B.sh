#!/usr/bin/env bash
if [[ $# < 3 || $# > 4 ]]; then
	echo Usage: $0 workload-file output-dir sd-size [switches]
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
sd_size=$(humanfriendly --parse-size=$3)
max_memory=$(humanfriendly --parse-size=1.1GB)
if [ $4 ]; then
	switches=$4
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-rocksdb/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "systemd-run --user -E LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 --scope -p MemoryMax=$max_memory $kvexe_dir/rocksdb-kvexe --cleanup --switches=$switches --num_threads=8 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=67108864 --optimize_filters_for_hits --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,1000000000000}}\" 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
