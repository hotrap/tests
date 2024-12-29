#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/kvexe-generic.sh "$2 $workspace/kvexe-rocksdb/build/rocksdb-kvexe" 320MiB $((12 * 64))MiB "$1" " --db_paths=\"{{$workspace/testdb/sd,10000000000000}}\" --cachelib_size=10000000000 --cachelib_ram_size=134217728 $3"
$workspace/tests/helper/rocksdb-data.sh "$1"
$workspace/tests/plot/hit-rate.py "$1"
