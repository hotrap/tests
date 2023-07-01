#!/usr/bin/env bash
if [[ $# != 4 ]]; then
	echo Usage: $0 sd-size max-hot-size workload-file output-dir
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
kvexe_dir=../../kvexe/build/Release
workload_file=$(realpath "$3")
DIR=$(realpath "$4")
# hit_count, kAccurateHotSizePromotionSize
ulimit -n 100000
(cd ../../YCSB && ./bin/ycsb load basic -P $workload_file) | $kvexe_dir/rocksdb-kvexe --cleanup --compaction_pri=6 --max_hot_set_size=$max_hot_set_size --switches=none --db_path=$HOME/testdb/db/ --db_paths="{{$HOME/testdb/sd,$sd_size},{$HOME/testdb/cd,100000000000}}" --viscnts_path=$HOME/testdb/viscnts > /dev/null 2>> $4/log.txt
cd ../../testdb/
du -sh db/ sd/ cd/ >> $DIR/log.txt
cd - > /dev/null

tmp_dir=$(mktemp -d)
occurrences=$(mktemp)
../helper/exe-while.sh $tmp_dir bash -c "(cd ../../YCSB && ./bin/ycsb run basic -P $workload_file) | tee >(../helper/bin/trace-cleaner | awk '{if (\$1 == \"READ\") print \$3}' | ../helper/bin/occurrences > $occurrences) | $kvexe_dir/rocksdb-kvexe --compaction_pri=6 --max_hot_set_size=$max_hot_set_size --switches=all --db_path=$HOME/testdb/db/ --db_paths=\"{{$HOME/testdb/sd,$sd_size},{$HOME/testdb/cd,100000000000}}\" --viscnts_path=$HOME/testdb/viscnts > /dev/null 2>> $4/log.txt"
sort -nk2 -r $occurrences > $4/occurrences
rm $occurrences
mv -n $tmp_dir/* $4/
rm -r $tmp_dir
bash ../helper/hotrap-data.sh "$DIR"
