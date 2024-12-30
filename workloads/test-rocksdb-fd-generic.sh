#!/usr/bin/env sh
if [ $# -lt 3 -o $# -gt 5 ]; then
	echo Usage: $0 cache-size L1-size output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath "$(dirname $0)"/../..)
L1_size=$(humanfriendly --parse-size="$2")
$(dirname $0)/kvexe-generic.sh "$4 $workspace/kvexe-rocksdb/build/rocksdb-kvexe" "$workspace/testdb/db" "$1" "$3" "--max_bytes_for_level_base=$L1_size --db_paths=\"{{$workspace/testdb/fd,10000000000000}}\" $5"
$workspace/tests/helper/rocksdb-data.sh "$3"
