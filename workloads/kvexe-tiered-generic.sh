#!/usr/bin/env sh
if [ $# -lt 5 -o $# -gt 6 ]; then
	echo Usage: $0 command cache-size fd-size L1-size output-dir [extra-kvexe-args]
	exit 1
fi
fd_size=$(humanfriendly --parse-size="$3")
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/kvexe-generic.sh "$1" "$2" "$4" "$5" "--db_paths=\"{{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}}\" $6"
