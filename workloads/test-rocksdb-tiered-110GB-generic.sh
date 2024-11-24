#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/test-rocksdb-tiered-generic.sh 192MiB 10GB $((12 * 64))MiB "$1" "$2" "--switches=0x1 $3"
