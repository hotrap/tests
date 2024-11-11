#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
./dbbench-1e7-rocksdb-plot.sh "$DIR" &
wait
