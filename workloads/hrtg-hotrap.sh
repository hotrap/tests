#!/usr/bin/env bash
if [[ $# < 4 || $# > 6 ]]; then
	echo Usage: $0 sd-size max-hot-size workload-file output-dir [num-threads] [switches]
	exit 1
fi
set -e
set -o pipefail
# To make set -e take effect if the output dir does not exists
mkdir -p $4
res="$(ls -A $4)"
if [ "$res" ]; then
    echo "$4" is not empty!
    exit 1
fi
sd_size=$(humanfriendly --parse-size=$1)
max_hot_set_size=$(humanfriendly --parse-size=$2)
if [ $5 ]; then
	num_threads=$5
else
	num_threads=1
fi
if [ $6 ]; then
	switches=$6
else
	switches=0x1
fi
kvexe_dir=../../kvexe/build/
# hit_count, kAccurateHotSizePromotionSize
ulimit -n 100000
../helper/exe-while.sh $4 bash -c "set -e; set -o pipefail; ../../trace-generator/target/release/trace-generator $3 | $kvexe_dir/rocksdb-kvexe --cleanup --format=plain --compaction_pri=5 --max_hot_set_size=$max_hot_set_size --switches=$switches --num_threads=$num_threads --db_path=../../testdb/db/ --db_paths=\"{{../../testdb/sd,$sd_size},{../../testdb/cd,100000000000}}\" --viscnts_path=../../testdb/viscnts 2>> $4/log.txt"
../../trace-generator/target/release/trace-generator $3 | awk '{if ($1 == "READ") print $2}' | ../helper/bin/occurrences > ../../testdb/db/occurrences
bash ../helper/hotrap-data.sh "$4"
