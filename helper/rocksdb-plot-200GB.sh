#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 50 &
wait
