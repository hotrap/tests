#!/usr/bin/env bash
if [[ $# < 4 || $# > 5 ]]; then
	echo Usage: $0 workload-file output-dir fd-size max-hot-size max-viscnts-size [switches]
	exit 1
fi
mkdir -p $2
res="$(ls -A $2)"
if [ "$res" ]; then
	echo "$2" is not empty!
	exit 1
fi
workload_file=$(realpath -s "$1")
DIR=$(realpath "$2")
fd_size=$(humanfriendly --parse-size=$3)
max_hot_set_size=$(humanfriendly --parse-size=$4)
max_viscnts_size=$(humanfriendly --parse-size=$5)
max_memory=$(humanfriendly --parse-size=1.1GB)
if [ $6 ]; then
	switches=$6
else
	switches=0x1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "systemd-run --user -E LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 --scope -p MemoryMax=$max_memory perf record --call-graph=fp -o $DIR/perf.data $kvexe_dir/rocksdb-kvexe --run --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=$switches --num_threads=8 --max_background_jobs=4 --block_size=16384 --max_bytes_for_level_base=67108864 --enable_fast_generator --enable_fast_process --workload_file=$workload_file --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts 2>> $DIR/log.txt"
bash ../helper/hotrap-data.sh "$DIR"
perf script -i $DIR/perf.data | inferno-collapse-perf > $DIR/perf.folded
