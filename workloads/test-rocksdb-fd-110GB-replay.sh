#!/usr/bin/env sh
if [ $# -lt 2 -o $# -gt 3 ]; then
	echo Usage: $0 trace-prefix output-dir [extra-kvexe-args]
	exit 1
fi
$(dirname $0)/replay.sh rocksdb-fd-110GB "$@"
