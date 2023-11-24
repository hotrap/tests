#!/usr/bin/env bash
if [[ $# < 4 || $# > 5 ]]; then
	echo Usage: $0 workload-file output-dir sd-size secondary-cache-size [switches]
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
secondary_cache_size=$(humanfriendly --parse-size=$4)
sd_size=$(($sd_size-$secondary_cache_size))
if [ $5 ]; then
	switches=$5
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe-secondary-cache/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "$kvexe_dir/rocksdb-kvexe --cleanup --switches=$switches --num_threads=8 --max_background_jobs=4 --block_size=16384 --cache_size=75497472 --max_bytes_for_level_base=67108864 --secondary_cache_size=$secondary_cache_size --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,1000000000000}}\" 2>> $DIR/log.txt"
bash ../helper/rocksdb-data.sh "$DIR"
