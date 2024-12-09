#!/usr/bin/env sh
if [ $# -ne 2 ]; then
	echo Usage: $0 command output-dir
	exit 1
fi
command="$1"
mkdir -p "$2"
DIR=$(realpath "$2")
if [ "$(ls -A $DIR)" ]; then
	echo "$2" is not empty!
	exit 1
fi
cd "$(dirname $0)"
workspace=$(realpath ../..)
fd_size=10000000000
# We need about 1.2e9 keys to make the DB size 110GB.
# But there may be overwrites, so the key space should be larger than the number of keys.
num=2000000000

memtable_size=$((64 * 1024 * 1024))
L1_size=$(($fd_size / 12 / $memtable_size * $memtable_size))

cd "$DIR"
ulimit -n 100000
# Dump core when crash
ulimit -c unlimited
rm -r $workspace/testdb/*/*
$command \
	--benchmarks=fillrandom \
	--compression_type=none \
	--compression_ratio=1 \
	--bloom_bits=10 \
	--use_direct_io_for_flush_and_compaction=true \
	--use_direct_reads=true \
	--key_size=48 \
	--value_size=43 \
	--db="$workspace/testdb/db" \
	--db_paths="[{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}]" \
	--max_background_jobs=6 \
	--block_size=16384 \
	--cache_size=134217728 \
	--max_bytes_for_level_base=$L1_size \
	--num=$num
$command \
	--use_existing_db=true \
	--benchmarks=levelstats \
	--compression_type=none \
	--db="$workspace/testdb/db" \
	--db_paths="[{$workspace/testdb/fd,$fd_size},{$workspace/testdb/sd,1000000000000}]" > levelstats-load-finish 2>&1
