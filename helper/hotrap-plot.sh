#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 dir
	exit 1
fi
DIR=$(realpath "$1")
cd $(dirname $0)
mkdir -p $DIR/plot/
./rocksdb-plot.sh $DIR &
../plot/promoted-or-retained-bytes.py $DIR &
../plot/hit-rate.py $DIR &
../plot/ralt-sizes.py $DIR &
../plot/vc-param.py $DIR &
wait
