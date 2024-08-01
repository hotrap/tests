#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 workload-file output-dir [extra-kvexe-args]
	exit 1
fi
workload_file=$(realpath $1)
mkdir -p $2
DIR=$(realpath "$2")
workspace=$(realpath ../..)
./test-rocksdb-fd-110GB-generic.sh "$2" "" "--load --enable_fast_generator --workload_file=$workload_file $3"
rm -r $DIR
mkdir $DIR
./test-rocksdb-fd-110GB-generic.sh "$2" "perf record --call-graph=fp -o $DIR/perf.data" "--run --enable_fast_generator --workload_file=$workload_file --switches=0x1 $3"
perf script -i $DIR/perf.data | inferno-collapse-perf > $DIR/perf.folded
