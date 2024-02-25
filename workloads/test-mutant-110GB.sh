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
../helper/exe-while.sh $DIR bash -c "systemd-run --user --scope -p MemoryMax=4G nocache $workspace/kvexe-mutant/build/rocksdb-kvexe --cleanup --format=ycsb --num_threads=16 --switches=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,$cd_size}}\" --costs=\"{0.528, 0.045}\" --target_cost=0.4 --enable_fast_process --enable_fast_generator --workload_file=$workload_file >/dev/null 2> $DIR/log.txt"
cp $workspace/testdb/db/{a*,b*,v*,d*,e*,f*,h*,g*,i*,j*,k*,l*,o*,p*,q*,r*,s*,t*,u*,v*,w*,x*,y*,z*,n*,m*,LOG,log.txt,cpu,first-level-in-sd,progress,promoted-*,rocksdb-stats.txt,period_stats,latency*,mem} $DIR/
../helper/last-10p-latency.py $DIR
