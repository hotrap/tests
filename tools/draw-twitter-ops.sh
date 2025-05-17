#!/usr/bin/env sh
if [ "$1" ]; then
	cd "$1"
fi
workspace=$(realpath $(dirname $0)/../..)
tests=$workspace/tests

data_dir=cluster29/prismdb
if [ -f $data_dir/info.json ]; then
	if [ ! "$(grep "run-end-timestamp" $data_dir/info.json)" ]; then
		echo "PrismDB crashes under cluster29. Using the last 10% of its completed run phase."
		printf "\t\"run-end-timestamp(ns)\": $(tail -n 1 $data_dir/progress | cut -d' ' -f1)\n}" >> $data_dir/info.json
	fi
fi
$tests/plot/twitter_ops.py .
