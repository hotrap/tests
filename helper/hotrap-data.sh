if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
set -e
DIR=$(realpath "$1")
cd $(dirname $0)
bash rocksdb-data.sh "$DIR"
cd ../../testdb
mv db/{first-level-in-cd,promoted-iter-bytes,promoted-get-bytes} "$DIR"/
mv viscnts/* "$DIR"/
