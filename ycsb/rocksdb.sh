#!/usr/bin/env bash
if [[ $# != 3 ]]; then
	echo Usage: $0 sd-size workload-file output-dir
	exit 1
fi
set -e
set -o pipefail
# To make set -e take effect if the output dir does not exists
mkdir -p $3
res="$(ls -A $3)"
if [ "$res" ]; then
        echo "$3" is not empty!
        exit 1
fi
sd_size=$(humanfriendly --parse-size=$1)
kvexe_dir=../../kvexe-rocksdb/build/Release
workload_file=$(realpath $2)
DIR=$(realpath "$3")
# SD=3GB
ulimit -n 100000
(cd ../../YCSB && ./bin/ycsb load basic -P $workload_file) | $kvexe_dir/rocksdb-kvexe --cleanup --db_path=../../testdb/db/ --db_paths="{{../../testdb/sd,$sd_size},{../../testdb/cd,100000000000}}" > /dev/null 2>> $3/log.txt
cd ../../testdb/
du -sh db/ sd/ cd/ >> $DIR/log.txt
cd - > /dev/null

tmp_dir=$(mktemp -d)
../helper/exe-while.sh $tmp_dir bash -c "set -e; set -o pipefail; (cd ../../YCSB && ./bin/ycsb run basic -P $workload_file) | $kvexe_dir/rocksdb-kvexe --switches=all --db_path=../../testdb/db/ --db_paths=\"{{../../testdb/sd,$sd_size},{../../testdb/cd,100000000000}}\" > /dev/null 2>> $3/log.txt"
mv -n $tmp_dir/* $3/
rm -r $tmp_dir
bash ../helper/rocksdb-data.sh "$DIR"
