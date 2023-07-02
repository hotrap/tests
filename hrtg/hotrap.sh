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
# hit_count, kAccurateHotSizePromotionSize
ulimit -n 100000
occurrences=$(mktemp)
../../trace-generator/target/release/trace-generator $3 | awk '{if ($1 == "READ") print $2}' | ../helper/bin/occurrences > $occurrences
../helper/exe-while.sh $4 bash -c "set -e; set -o pipefail; ../../trace-generator/target/release/trace-generator $3 | $kvexe_dir/rocksdb-kvexe --cleanup --format=plain --compaction_pri=6 --max_hot_set_size=$max_hot_set_size --switches=all --db_path=$HOME/testdb/db/ --db_paths=\"{{$HOME/testdb/sd,$sd_size},{$HOME/testdb/cd,100000000000}}\" --viscnts_path=$HOME/testdb/viscnts 2>> $4/log.txt | sha256sum > $4/ans.sha256"
sort -nk2 -r $occurrences > $4/occurrences
rm $occurrences
bash ../helper/hotrap-data.sh "$4"
if [ -f $4/../testdb/ans.sha256 ]; then
	if cmp $4/ans.sha256 $4/../testdb/ans.sha256; then
		echo "cmp $4/ans.sha256 $4/../testdb/ans.sha256" > $4/compared
	fi
fi
