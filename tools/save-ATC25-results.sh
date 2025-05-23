#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: $0 dir
	exit 1
fi
dir=$(realpath "$1")
mkdir -p "$dir"

save() {
	if [ -f "$1" ]; then
		cp "$1" "$dir"
	fi
}
save fig5-ycsb-sweep.pdf
save fig6-ops-200B.pdf
save fig7-latency.pdf
save fig8-twitter-scatter.pdf
save fig9-twitter-speedup.pdf
save fig10-twitter-ops.pdf
save fig11-cputime-breakdown-200B.pdf
save fig12-io-breakdown-200B.pdf
save fig13-progress-hit-rate-hotspot0.05.pdf
save u24685531/hotrap/plot/fig14-dynamic-workload.pdf
save fig15-ops-1.1TB.pdf

save read_0.75_insert_0.25_hotspot0.05_110GB_220GB/table4-no-hotness-aware-compaction.tex
save ycsbc_uniform_110GB_220GB/table5-promote-accessed.tex
