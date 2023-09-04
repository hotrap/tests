if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
set -e
DIR=$(realpath "$1")
mydir=$(realpath $(dirname $0))
cd $mydir
bash rocksdb-data.sh "$DIR"
cd ../../testdb
cd db
sort -nk2 -r occurrences > occurrences_sorted_by_count
$mydir/hit . > "$DIR"/hit
mv promoted-2sdlast-bytes promoted-flush-bytes "$DIR"/
cd ..
mv viscnts/* "$DIR"/
