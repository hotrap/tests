#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
mkdir -p $1
DIR=$(realpath "$1")
if [ "$(ls -A $DIR)" ]; then
	echo "$1" is not empty!
	exit 1
fi
prefix="$2"
extra_kvexe_args="$3"
cd "$(dirname $0)"
workspace=$(realpath ../..)
kvexe_dir=$workspace/kvexe/build/

fd_size=10000000000
max_hot_set_size=5000000000
max_viscnts_size=1500000000
memtable_size=$((64 * 1024 * 1024))
L1_size=$((($fd_size - $max_viscnts_size) / 12 / $memtable_size * $memtable_size))

ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
cd $DIR
$workspace/tests/helper/exe-while.sh . sh -c "$prefix $kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --num_threads=16 --max_background_jobs=8 --block_size=16384 --cache_size=134217728 --max_bytes_for_level_base=$L1_size --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts --enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size $extra_kvexe_args 2>> log.txt"
$workspace/tests/helper/hotrap-data.sh .
