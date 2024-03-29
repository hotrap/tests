#!/usr/bin/env bash

if [ ! $2 ]; then
	echo Usage: $0 output-dir command [[args]] 2>&1
	exit 1
fi

if [ ! -d $1 ]; then
	mkdir -p $1
fi

set -m
(
	pgid=$(exec sh -c 'echo "$PPID"')
	(
		set -m
		"$(dirname $0)"/periodic-exe.sh $1 1>&2 &
		PID=$!
		function exit_fn {
			if [ $PID ]; then
				kill $PID
			fi
		}
		trap exit_fn EXIT
		wait $PID
		echo exe-while: periodic-exe exits early, exiting... 1>&2
		unset PID
		kill -TERM -$pgid
	) &
	bgpid=$!
	trap "kill -TERM $bgpid" EXIT
	$2 "${@:3}"
)
