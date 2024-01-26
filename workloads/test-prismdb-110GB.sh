#!/usr/bin/env bash
if [[ ! $2 ]]; then
	echo Usage: $0 workload-file output-dir
	exit 1
fi
mkdir -p $2
res="$(ls -A $2)"
if [ "$res" ]; then
	echo "$2" is not empty!
	exit 1
fi
workload_file=$(realpath -s "$1")
DIR=$(realpath "$2")
sd_size=12179869184
cd_size=1073741824000
cd "$(dirname $0)"
workspace=$(realpath ../..)

ulimit -n 100000
../helper/exe-while.sh $DIR bash -c "systemd-run --user --scope -p MemoryMax=4G nocache $workspace/kvexe-prismdb/build/rocksdb-kvexe --num_threads=16 --cache_size=75497472 --cleanup --format=ycsb --db_path=$workspace/testdb/cd --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,$cd_size}}\" --switches=1 --migrations_logging=1 --read_logging=0 --migration_policy=2 --migration_metric=1 --migration_rand_range_num=8 --migration_rand_range_size=1 --num_load_ops=200000000 --num_keys=110000000 --optane_threshold=0.1 --slab_dir=$workspace/testdb/sd/slab-%d-%lu-%lu --pop_cache_size=22000000 --enable_fast_generator --workload_file=$workload_file --read_dominated_threshold=0.95 --stop_upsert_trigger=70000000 2> $DIR/log.txt"
cp $workspace/testdb/cd/{a*,b*,v*,d*,e*,f*,h*,g*,i*,j*,k*,l*,o*,p*,q*,r*,s*,t*,u*,v*,w*,x*,y*,z*,n*,m*,LOG,log.txt,cpu,first-level-in-cd,progress,promoted-*,rocksdb-stats.txt,period_stats,latency*,mem} $DIR/
../helper/last-10p-latency.py $DIR
