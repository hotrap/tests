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
# cache_size=0, SD=3GB
ulimit -n 100000
../helper/exe-while.sh $3 bash -c "../../trace-generator/target/release/trace-generator $2 | $kvexe_dir/rocksdb-kvexe --cleanup --format=plain --switches=all --cache_size=0 --db_path=$HOME/testdb/db/ --db_paths=\"{{$HOME/testdb/sd,$sd_size},{$HOME/testdb/cd,100000000000}}\" 2>> $3/log.txt | sha256sum > $3/ans.sha256"
bash ../helper/rocksdb-data.sh "$3"
