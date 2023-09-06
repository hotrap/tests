#!/usr/bin/env bash
# Execute this script in the root of hotrap-tests
if [ ! $1 ]; then
	echo Usage: $0 workload-name
	exit 1
fi
set -e
if [ -e ../data/$1 ]; then
	if [ ! -d ../data/$1 ]; then
		echo $(realpath ../data/$1) is not a directory!
		exit 1
	fi
	if [ "$(ls -A ../data/$1)" ]; then
		echo $(realpath ../data/$1) is not empty!
		exit 1
	fi
fi
helper/run-rocksdb $1
helper/run-hotrap $1 flush-accessed
helper/run-hotrap $1 flush-stably-hot
