if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
set -e
DIR=$(realpath "$1")
cd $(dirname $0)
cd ../../testdb
du -sh db/ sd/ cd/ >> "$DIR"/log.txt
mv db/{LOG,rocksdb-stats.txt,progress,latency,cpu} "$DIR"/
cd db
if [ -f ans_0 ]; then
	sha256sum ans_* > "$DIR"/ans.sha256
fi
