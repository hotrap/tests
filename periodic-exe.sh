#!/usr/bin/env bash

if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit
fi

cd jobs-periodic
works=$(ls)
for work in $works; do
	./$work >> $1/"$work.txt" &
done
trap "kill -TERM -$$" EXIT
wait
