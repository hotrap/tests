#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/kvexe-tiered-generic.sh "$2 systemd-run --user --scope -p MemoryMax=4G nocache $workspace/kvexe-rocksdb/build/rocksdb-kvexe" 192MiB 10GB $((12 * 64))MiB "$1" "--switches=0x1 --costs=\"{0.528, 0.045}\" --target_cost=0.4 $3"
$workspace/tests/helper/rocksdb-data.sh "$1"
