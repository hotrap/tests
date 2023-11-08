#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
DIR=$(realpath "$1")
mydir=$(realpath $(dirname $0))
cd $mydir
bash rocksdb-data.sh "$DIR"
cd ../../testdb
cd db
if [ -f occurrences ]; then
	sort -nk2 -r occurrences > occurrences_sorted_by_count
	$mydir/hit . > "$DIR"/hit
fi
mv first-level-in-cd promoted-or-retained-bytes not-promoted-bytes num-accesses "$DIR"/
cd ..
find viscnts/ -mindepth 1 -maxdepth 1 -print0 | xargs -0 -r mv -t "$DIR"/
