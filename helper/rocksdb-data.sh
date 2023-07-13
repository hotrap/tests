if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
set -e
DIR=$(realpath "$1")
cd $(dirname $0)
cd ../../testdb
du -sh db/ sd/ cd/ >> "$DIR"/log.txt
mv db/{rocksdb-stats.txt,progress,latency,cpu} "$DIR"/
if [ -f db/ans_1 ]; then
	mv db/ans_* "$DIR"/
fi
