if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
set -e
bash "$(dirname $0)"/rocksdb-data.sh "$1"
DIR=$(realpath "$1")
cd ../../testdb
mv db/{first-level-in-cd,promoted-iter-bytes,promoted-get-bytes} "$DIR"/
mv viscnts/* "$DIR"/
