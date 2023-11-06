#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
mkdir -p $DIR/plot/
bash rocksdb-plot-11GB.sh $DIR &
../plot/hit.py $DIR &
../plot/promoted-or-retained-bytes.py $DIR &
../plot/hit-rate.py $DIR &
wait
