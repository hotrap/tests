#!/usr/bin/env sh
if [ "$1" ]; then
	cd "$1"
fi
workspace=$(realpath $(dirname $0)/../..)
tests=$workspace/tests

if [ -d ycsbc_zipfian_110GB_220GB ]; then
	$tests/plot/ycsb-sweep.py .
	$tests/plot/ops-200B.py .
	$tests/tex/overhead-uniform-rocksdb-tiered.py .
	$tests/plot/latency.py .

	$tests/plot/cputime-breakdown-200B.py .
	$tests/plot/io-breakdown-200B.py .

	cd read_0.75_insert_0.25_hotspot0.05_110GB_220GB
	$tests/tex/table-no-hotness-aware-compaction.py .
	cd ..

	cd ycsbc_uniform_110GB_220GB
	$tests/tex/table-promote-accessed.py .
	cd ..

	$tests/plot/ops-1.1TB.py .
fi

if [ -d read_0.95_insert_0.05_hotspot0.05_110GB_220GB ]; then
	$tests/plot/progress-hit-rate.py .
fi

if [ -d u24685531/hotrap ]; then
	cd u24685531/hotrap
	$tests/plot/dymanic-workload.py .
	cd ../..
fi

if [ -d cluster02-283x ]; then
	$tests/plot/twitter_speedup.py . $workspace/twitter/processed
fi

if [ -d cluster17-80x/rocksdb-fd ]; then
	data_dir=cluster29/prismdb
	if [ ! "$(grep "run-end-timestamp" $data_dir/info.json)" ]; then
		echo "PrismDB crashes under cluster29. Using the last 10% of its completed run phase."
		echo -e "\t\"run-end-timestamp(ns)\": $(tail -n 1 $data_dir/progress | cut -d' ' -f1)\n}" >> $data_dir/info.json
	fi
	$tests/plot/twitter_ops.py .
fi
