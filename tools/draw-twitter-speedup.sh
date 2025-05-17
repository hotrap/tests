#!/usr/bin/env sh
if [ "$1" ]; then
	cd "$1"
fi
workspace=$(realpath $(dirname $0)/../..)
tests=$workspace/tests

$tests/plot/twitter_speedup.py . $workspace/twitter/processed

