#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: $0 workload
	exit 1
fi
workload=$1

twitter_dir=$(dirname $0)/../../twitter/processed
if [ ! "$twitter_zst_dir" ]; then
	twitter_zst_dir=$twitter_dir
fi

mkdir -p "$twitter_dir"

if [ ! -f "$twitter_dir/$workload.json" ]; then
	cp "$twitter_zst_dir/$workload.json" $twitter_dir/
fi
if [ ! -f "$twitter_dir/$workload-load" ]; then
	unzstd "$twitter_zst_dir/$workload-load.zst" --output-dir-flat $twitter_dir
fi
if [ ! -f "$twitter_dir/$workload-run" ]; then
	unzstd "$twitter_zst_dir/$workload-run.zst" --output-dir-flat $twitter_dir
fi
