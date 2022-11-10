#!/usr/bin/env bash

set -e

if [ ! $2 ]; then
	echo Usage: $0 command output-dir
	exit
fi

if [ ! -d $2 ]; then
	mkdir -p $2
fi

if [ "$(ls -A $2)" ]; then
	echo $2 is not empty!
	exit
fi

PID=$(set -m; ./periodic-exe.sh $2 > /dev/null & echo $!)
$1
kill $PID
