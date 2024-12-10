#!/usr/bin/env sh
if [ $# -lt 1 -o $# -gt 2 ]; then
	echo Usage: $0 output-dir num-op
	exit 1
fi
mkdir -p "$1"
DIR=$(realpath "$1")
if [ "$(ls -A $DIR)" ]; then
	echo "$1" is not empty!
	exit 1
fi
num_op="$2"
cd "$(dirname $0)"
workspace=$(realpath ../..)
fd_size=10000000000
db_bench=$workspace/rocksdb/build/db_bench
# We need about 1.2e9 keys to make the DB size 110GB.
# But there may be overwrites, so the key space should be larger than the number of keys.
num=2000000000

memtable_size=$((64 * 1024 * 1024))
L1_size=$(($fd_size / 12 / $memtable_size * $memtable_size))

time ./dbbench-load.sh $db_bench "$DIR"

cd "$DIR"
ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
$workspace/tests/helper/exe-while.sh . $db_bench \
	--use_existing_db=true \
	--benchmarks="mixgraph" \
	--compression_type=none \
	--compression_ratio=1 \
	--bloom_bits=10 \
	--ttl_seconds=0 \
	--use_direct_io_for_flush_and_compaction=true \
	--use_direct_reads=true \
	--keyrange_dist_a=14.18 \
	--keyrange_dist_b=-2.917 \
	--keyrange_dist_c=0.0164 \
	--keyrange_dist_d=-0.08082 \
	--keyrange_num=30 \
	--value_k=0.2615 \
	--value_sigma=25.45 \
	--iter_k=2.517 \
	--iter_sigma=14.236 \
	--mix_get_ratio=0.83 \
	--mix_put_ratio=0.14 \
	--mix_seek_ratio=0.03 \
	--sine_mix_rate_interval_milliseconds=5000 \
	--sine_mix_rate=true \
	--sine_a=1000 \
	--sine_b=0.000073 \
	--sine_d=4500 \
	--perf_level=2 \
	--key_size=48 \
	--db="$workspace/testdb/db" \
	--db_paths="[{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}]" \
	--num=$num \
	--threads=16 \
	--max_background_jobs=6 \
	--block_size=16384 \
	--cache_size=134217728 \
	--max_bytes_for_level_base=$L1_size \
	--reads=$(($num_op / 16)) \
	--statistics=true \
	--report_file="$DIR/report.csv" \
	--report_interval_seconds=1 \
	--histogram=true \
	--report_operation_count_time=true >> log.txt
$workspace/tests/helper/dbbench-rocksdb-data.sh .
