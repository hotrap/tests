#!/usr/bin/env bash
if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
DIR=$(realpath "$1")
mydir=$(realpath $(dirname $0))
cd $mydir
cd ../../testdb
du -sh db/ sd/ cd/ >> "$DIR"/log.txt
cd db
if [ -f occurrences ]; then
	sort -nk2 -r occurrences > occurrences_sorted_by_count
	$mydir/hit . "$DIR"
fi
find . \
	-mindepth 1 \
	\! -regex "\./[0-9]*\.log" \
	\! -name CURRENT \
	\! -name IDENTITY \
	\! -name LOCK \
	\! -regex "\./MANIFEST-[0-9]*" \
	\! -regex "\./OPTIONS-[0-9]*\.dbtmp" \
	-exec mv {} "$DIR" \;
cd ..
find viscnts/ -mindepth 1 -maxdepth 1 -print0 | xargs -0 -r mv -t "$DIR"/
