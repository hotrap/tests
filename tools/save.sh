#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: $0 paper-dir
	exit 1
fi

paper_dir=$1
mkdir -p "$paper_dir"/fig
mkdir -p "$paper_dir"/data
if [ -f ycsb-sweep.pdf ]; then
	cp ycsb-sweep.pdf "$paper_dir"/fig/
	cp ycsb-sweep.tex "$paper_dir"/data/
	cp ops-200B.pdf "$paper_dir"/fig/
	cp overhead-uniform-rocksdb-tiered.tex "$paper_dir"/data/
	cp latency.pdf "$paper_dir"/fig

	cp cputime-breakdown-200B.pdf "$paper_dir"/fig/
	cp cpu-breakdown-200B.tex "$paper_dir"/data/
	cp io-breakdown-200B.pdf "$paper_dir"/fig/
	cp io-breakdown-200B.tex "$paper_dir"/data/

	cd read_0.75_insert_0.25_hotspot0.05_110GB_220GB
	cp table-no-hotness-aware-compaction.tex "$paper_dir"/data/
	cd ..

	cd ycsbc_uniform_110GB_220GB
	cp table-promote-accessed.tex promote-accessed.tex "$paper_dir"/data/
	cd ..

	cp ops-1.1TB.pdf "$paper_dir"/fig/
fi

if [ -f progress-hit-rate-hotspot0.05.pdf ]; then
	cp progress-hit-rate-hotspot0.05.pdf "$paper_dir"/fig/
fi

if [ -f u24685531/hotrap/plot/dynamic-workload.pdf ]; then
	cp u24685531/hotrap/plot/dynamic-workload.pdf "$paper_dir"/fig/
fi

if [ -f twitter-speedup.pdf ]; then
	cp twitter-speedup.pdf ~/sshfs/paper/fig/
	cp twitter-speedup.tex ~/sshfs/paper/data/
fi

if [ -f twitter-ops.pdf ]; then
	cp twitter-ops.pdf ~/sshfs/paper/fig/
	cp twitter.tex ~/sshfs/paper/data/
fi
