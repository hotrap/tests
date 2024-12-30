#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: $0 workload
	exit 1
fi
workload=$1

if [ "$twitter_delete_uncompressed" ]; then
	twitter_dir=../../twitter/processed
	rm $twitter_dir/$workload-load $twitter_dir/$workload-run
fi
