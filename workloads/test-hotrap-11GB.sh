#!/usr/bin/env bash
if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
	exit 1
fi
$(dirname $0)/test-hotrap-11GB-generic.sh "$2" "--workload_file=$1 --switches=0x1 $3"
