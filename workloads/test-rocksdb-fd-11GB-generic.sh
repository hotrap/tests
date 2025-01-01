#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath ../..)
$(dirname $0)/test-rocksdb-fd-generic.sh 320MiB 64MiB "$1" "$2" "--level0_file_num_compaction_trigger=1 $3"
