#!/usr/bin/env sh
if [ "$1" ]; then
	cd "$1"
fi
workspace=$(realpath $(dirname $0)/../..)
tests=$workspace/tests

$tests/plot/ops-200B.py .
$tests/plot/cputime-breakdown-200B.py .
$tests/plot/io-breakdown-200B.py .
