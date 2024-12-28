#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 3 ]; then
	echo Usage: $0 output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
$(dirname $0)/test-hotrap-generic.sh 5GB 1.5GB 256MiB 10GB $((12 * 64))MiB "$@"
