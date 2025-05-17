#!/usr/bin/env sh
if [ "$1" ]; then
	cd "$1"
fi
workspace=$(realpath $(dirname $0)/../..)
tests=$workspace/tests

if [ -d ycsbc_zipfian_110GB_220GB ]; then
	$tests/plot/ycsb-sweep.py .
	$tests/tex/overhead-uniform-rocksdb-tiered.py .
	$tests/plot/latency.py .

	cd read_0.75_insert_0.25_hotspot0.05_110GB_220GB
	$tests/tex/table-no-hotness-aware-compaction.py .
	cd ..

	cd ycsbc_uniform_110GB_220GB
	$tests/tex/table-promote-accessed.py .
	cd ..

	$tests/tools/draw-200B.sh

	$tests/plot/ops-1.1TB.py .
fi

if [ -d read_0.9_insert_0.1_hotspot0.05_110GB_220GB ]; then
	$tests/plot/progress-hit-rate.py .
fi

if [ -d u24685531/hotrap ]; then
	cd u24685531/hotrap
	$tests/plot/dymanic-workload.py .
	cd ../..
fi

if [ -d cluster02-283x ]; then
	$tests/tools/draw-twitter-speedup.sh
fi

if [ -d cluster17-80x/rocksdb-fd ]; then
	$tests/tools/draw-twitter-ops.sh
fi
