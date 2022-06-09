#!/usr/bin/env bash

if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit
fi

cd jobs-periodic
works=$(ls)
for work in $works; do
	#if [ -x "$work" ]; then
	#if [ -x "$work" -a -f "$work" ]; then
	if [[ -x "$work" && -f "$work" ]]; then
		./$work >> $1/"$work.txt" &
	fi
done
trap "kill -TERM -$$" EXIT
wait
