#!/usr/bin/env sh
if [ $# -lt 6 -o $# -gt 8 ]; then
	echo Usage: $0 max-hot-set-size max-ralt-size cache-size fd-size L1-size output-dir [prefix] [extra-kvexe-args]
	exit 1
fi
max_hot_set_size=$(humanfriendly --parse-size="$1")
max_ralt_size=$(humanfriendly --parse-size="$2")
workspace=$(realpath "$(dirname $0)"/../..)
$(dirname $0)/kvexe-tiered-generic.sh "$7 $workspace/kvexe/build/rocksdb-kvexe" "$3" "$4" "$5" "$6" \
	"--compaction_pri=5 \
--max_hot_set_size=$max_hot_set_size \
--max_ralt_size=$max_ralt_size \
--ralt_path=$workspace/testdb/ralt \
--enable_auto_tuning $8"
$workspace/tests/helper/hotrap-data.sh "$6"
