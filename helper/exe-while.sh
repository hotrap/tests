#!/usr/bin/env bash

set -e

if [ ! $2 ]; then
	echo Usage: $0 output-dir command [[args]]
	exit 1
fi

if [ ! -d $1 ]; then
	mkdir -p $1
fi

if [ "$(ls -A $1)" ]; then
	echo $1 is not empty!
	exit 1
fi

PID=$(set -m; "$(dirname $0)"/periodic-exe.sh $1 > /dev/null & echo $!)
trap "kill $PID" EXIT
$2 "${@:3}"
