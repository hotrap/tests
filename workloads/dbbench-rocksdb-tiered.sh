#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
$(dirname $0)/dbbench-rocksdb-tiered-generic.sh "$1" 420000000
