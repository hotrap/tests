#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: $0 dir
	exit 1
fi
dir=$1
$(dirname $0)/save-ATC25-results.sh "$dir"

save() {
	if [ -f "$1" ]; then
		cp "$1" "$dir"
	fi
}
save ycsb-sweep.tex
save overhead-uniform-rocksdb-tiered.tex
save cpu-breakdown-200B.tex
save io-breakdown-200B.tex
save ycsbc_uniform_110GB_220GB/promote-accessed.tex
save twitter-speedup.tex
save twitter.tex
