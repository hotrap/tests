#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload output-dir [extra-kvexe-args]
	exit 1
fi
workspace=$(realpath ../..)
$(dirname $0)/test-rocksdb-fd-11GB-generic.sh "$2" "--load=$workspace/YCSB-traces/$1-load --run=$workspace/YCSB-traces/$1-run --format=plain-length-only --export_ans_xxh64 --switches=0x1 $3"
