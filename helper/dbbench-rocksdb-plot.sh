#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
mkdir -p "$DIR"/plot/
../plot/dbbench-ops.py "$DIR" &
../plot/dbbench-latency.py "$DIR" 10 &
wait
