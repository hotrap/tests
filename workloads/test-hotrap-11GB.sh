#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
	exit 1
fi
workload_file=$(realpath -s "$1")
$(dirname $0)/test-hotrap-11GB-generic.sh "$2" "--enable_fast_generator --workload_file=$workload_file --switches=0x1 $3"
