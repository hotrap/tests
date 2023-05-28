#!/usr/bin/env bash

set -e

if [ ! $2 ]; then
	echo Usage: $0 output-dir command [[args]]
	exit
fi

if [ ! -d $1 ]; then
	mkdir -p $1
fi

if [ "$(ls -A $1)" ]; then
	echo $1 is not empty!
	exit
fi

PID=$(set -m; ./periodic-exe.sh $1 > /dev/null & echo $!)
$2 ${@:3}
kill $PID
