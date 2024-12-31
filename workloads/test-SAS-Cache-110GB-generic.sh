#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath $(dirname $0)/../..)
$(dirname $0)/kvexe-generic.sh "$2 $workspace/kvexe-rocksdb/build/rocksdb-kvexe" "$workspace/testdb/db" 320MiB "$1" "--max_bytes_for_level_base=$((12 * 64 * 1024 * 1024)) --db_paths=\"{{$workspace/testdb/sd,10000000000000}}\" --secondary_cache_size_MiB=10000 $3"
$workspace/tests/helper/rocksdb-data.sh "$1"
