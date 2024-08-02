#!/usr/bin/env sh

workspace=$(realpath ../..)

. ../helper/common.sh

checkout() {
	cd $workspace/hotrap
	git checkout main
	build_rocksdb

	cd ../RALT
	build_ralt "$1"

	cd ../kvexe
	git checkout main
	build_kvexe_ralt

	cd $workspace/tests/workloads
}

workload="read_0.5_insert_0.5_hotspot0.05_110GB"

test_hotrap() {
	mkdir -p $1
	DIR=$(realpath "$1")
	if [ "$(ls -A $DIR)" ]; then
		echo "$1" is not empty!
		exit 1
	fi
	workload_file=$(realpath -s "../config/$workload")
	kvexe_dir=$workspace/kvexe/build/

	fd_size=10000000000
	max_hot_set_size=5500000000
	max_viscnts_size=500000000
	memtable_size=$((64 * 1024 * 1024))
	L1_size=$((($fd_size - $max_viscnts_size) / 12 / $memtable_size * $memtable_size))

	ulimit -n 100000
	cd $DIR
	$workspace/tests/helper/exe-while.sh . sh -c "$kvexe_dir/rocksdb-kvexe --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --max_viscnts_size=$max_viscnts_size --num_threads=16 --max_background_jobs=8 --block_size=16384 --cache_size=134217728 --max_bytes_for_level_base=$L1_size --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,100000000000}}\" --viscnts_path=$workspace/testdb/viscnts --enable_fast_generator --workload_file=$workload_file --switches=0x1 2>> log.txt"
	$workspace/tests/helper/hotrap-data.sh .
	cd - > /dev/null
}

run() {
	if [ $1 = "EXP" ]; then
		checkout
	else
		checkout "-DUSE_$1=ON"
	fi
	DIR=../../data/$workload/$1
	echo Result directory: $DIR
	test_hotrap $DIR
	../helper/hotrap-plot.sh $DIR
}

run "CLOCK"
run "LRU"

cd $workspace/RALT
rm -r build
run "EXP"

