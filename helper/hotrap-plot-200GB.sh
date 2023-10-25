#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
mkdir -p $DIR/plot/
bash rocksdb-plot-200GB.sh $DIR &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
../plot/hit-rate.py $DIR &
wait
