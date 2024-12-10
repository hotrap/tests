#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
mkdir -p "$DIR"/plot/
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 1 &
../plot/dbbench-report.py "$DIR" &
../plot/dbbench-latency.py "$DIR" 1 &
wait
