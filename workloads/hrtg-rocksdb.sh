#!/usr/bin/env bash
if [[ $# < 3 || $# > 5 ]]; then
	echo Usage: $0 sd-size workload-file output-dir [num-threads] [switches]
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
if [ $4 ]; then
	num_threads=$4
else
	num_threads=1
fi
if [ $5 ]; then
	switches=$5
else
	switches=0x0
fi
kvexe_dir=../../kvexe-rocksdb/build/
# cache_size=0, SD=3GB
ulimit -n 100000
../helper/exe-while.sh $3 bash -c "set -e; set -o pipefail; ../../trace-generator/target/release/trace-generator $2 | $kvexe_dir/rocksdb-kvexe --cleanup --format=plain --switches=$switches --num_threads=$num_threads --max_background_jobs=4 --level0_file_num_compaction_trigger=1 --db_path=../../testdb/db/ --db_paths=\"{{../../testdb/sd,$sd_size},{../../testdb/cd,100000000000}}\" 2>> $3/log.txt"
bash ../helper/rocksdb-data.sh "$3"
