#!/usr/bin/env bash
if [[ $# < 3 || $# > 4 ]]; then
	echo Usage: $0 trace-file-load trace-file-run output-dir [extra-kvexe-args]
	exit 1
fi
trace_file_load=$(realpath -s "$1")
trace_file_run=$(realpath -s "$2")
mkdir -p $3
DIR=$(realpath "$3")
if [ "$(ls -A $DIR)" ]; then
	echo "$3" is not empty!
	exit 1
fi
extra_kvexe_args="$4"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_path=$workspace/kvexe/build/rocksdb-kvexe

fd_size=10000000000
max_hot_set_size=5000000000
max_viscnts_size=1500000000
memtable_size=$((64 * 1024 * 1024))
L1_size=$((($fd_size - $max_viscnts_size) / 12 / $memtable_size * $memtable_size))

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . bash -c "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 $kvexe_path --load=$trace_file_load --run=$trace_file_run --format=plain-length-only --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --switches=0x1 --num_threads=16 --max_background_jobs=8 --block_size=16384 --cache_size=134217728 --max_bytes_for_level_base=$L1_size --enable_fast_process --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts --enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size $extra_kvexe_args 2>> log.txt"
bash $workspace/tests/helper/hotrap-data.sh .
