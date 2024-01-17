cd "$(dirname $0)"
workspace=$(realpath ../..)
sd_size=12179869184
cd_size=1073741824000

workloads=(
	"workload_110GB_wr_hotspot0.05"
	"workload_110GB_wr_uniform"
	"workload_110GB_wr_zipfian"
	"workload_110GB_wh_hotspot0.05"
	"workload_110GB_wh_uniform"
	"workload_110GB_wh_zipfian"
	"workload_110GB_ycsba_hotspot0.05"
	"workload_110GB_ycsba_uniform"
	"workload_110GB_ycsba_zipfian"
	"workload_110GB_ycsbc_hotspot0.05"
	"workload_110GB_ycsbc_uniform"
	"workload_110GB_ycsbc_zipfian"
)

function store {
	cp ~/testdb/db/{a*,b*,v*,d*,e*,f*,h*,g*,i*,j*,k*,l*,o*,p*,q*,r*,s*,t*,u*,v*,w*,x*,y*,z*,n*,m*,LOG,log.txt,cpu,first-level-in-cd,progress,promoted-*,rocksdb-stats.txt,period_stats,latency*,mem} $1/
}

function run-prismdb {
	../helper/checkout-prismdb
	workload_file=$(realpath -s "../config/$1")
	DIR=../../data/$1/prismdb
	../helper/exe-while.sh $DIR bash -c "systemd-run --user --scope -p MemoryMax=4G nocache $workspace/kvexe-prismdb/build/rocksdb-kvexe --num_threads=8 --cache_size=75497472 --cleanup --format=ycsb --db_path=$workspace/testdb/db --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,$cd_size}}\" --switches=1 --migrations_logging=1 --read_logging=0 --migration_policy=2 --migration_metric=1 --migration_rand_range_num=8 --migration_rand_range_size=1 --num_load_ops=200000000 --num_keys=110000000 --optane_threshold=0.1 --slab_dir=$workspace/testdb/sd/slab-%d-%lu-%lu --pop_cache_size=22000000 --enable_fast_generator --workload_file=$workload_file --read_dominated_threshold=0.95 --stop_upsert_trigger=70000000 2> $DIR/log.txt"
	store $DIR
}

function run-mutant {
	../helper/checkout-mutant
	workload_file=$(realpath -s "../config/$1")
	DIR=../../data/$1/mutant
	../helper/exe-while.sh $DIR bash -c "systemd-run --user --scope -p MemoryMax=4G nocache $workspace/kvexe-mutant/build/rocksdb-kvexe --cleanup --format=ycsb --num_threads=8 --switches=1 --db_path=$workspace/testdb/db/ --db_paths=\"{{$workspace/testdb/sd,$sd_size},{$workspace/testdb/cd,$cd_size}}\" --costs=\"{0.528, 0.045}\" --target_cost=0.4 --enable_fast_process --enable_fast_generator --workload_file=$workload_file >/dev/null 2> $DIR/log.txt"
	store $DIR
}

for workload in "${workloads[@]}"; do
	run-prismdb $workload
	run-mutant $workload
done
