#!/usr/bin/env bash

if [ ! $2 ]; then
	echo Usage: $0 command output-dir
	exit
fi

PID=$(set -m; ./periodic-exe.sh $2 > /dev/null & echo $!)
$1
kill $PID
