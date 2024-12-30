#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/kvexe-generic.sh "$2 $workspace/kvexe-rocksdb/build/rocksdb-kvexe" "$workspace/testdb/sd" 320MiB "$1" "--db_paths=\"{{$workspace/testdb/fd,12179869184},{$workspace/testdb/sd,10000000000000}}\" --migrations_logging=1 --read_logging=0 --migration_policy=2 --migration_metric=1 --migration_rand_range_num=8 --migration_rand_range_size=1 --optane_threshold=0.1 --slab_dir=$workspace/testdb/fd/slab-%d-%lu-%lu --pop_cache_size=22000000 --read_dominated_threshold=0.95 $3"
$workspace/tests/helper/save-common-data.sh "$workspace/testdb/sd" "$1"
$workspace/tests/helper/last-10p-latency.py "$1"
