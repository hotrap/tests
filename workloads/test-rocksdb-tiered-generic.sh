#!/usr/bin/env sh
if [ $# -lt 4 -o $# -gt 6 ]; then
	echo Usage: $0 cache-size fd-size L1-size output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/kvexe-tiered-generic.sh "$5 $workspace/kvexe-rocksdb/build/rocksdb-kvexe" "$1" "$2" "$3" "$4" "$6"
$workspace/tests/helper/rocksdb-data.sh "$4"
