#!/usr/bin/env bash
if [ ! $2 ]; then
	echo Usage: $0 std-dir ans-dir
	exit 1
fi

i=0
while [ -f $1/ans-$i.xxh64 ]; do
	diff $1/ans-$i.xxh64 $2/ans-$i.xxh64
	i=$(($i + 1))
done
