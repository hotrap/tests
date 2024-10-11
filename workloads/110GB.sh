workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)
function run-rocksdb-fd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-fd
	echo Result directory: $DIR
	./test-rocksdb-fd-110GB.sh ../config/$1 $DIR "$2"
	../helper/rocksdb-plot.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-$2-110GB.sh ../config/$1 $DIR "$3"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR "$3"
	../helper/hotrap-plot.sh $DIR
}
function run-workload {
	workload=$1
	../helper/checkout-hotrap
	DIR=../../data/$workload/hotrap
	echo Result directory: $DIR
	./test-hotrap-110GB-generic.sh $DIR "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--enable_fast_generator --workload=$workload --switches=0x1"
	../helper/hotrap-plot.sh $DIR
}

for workload in "${workloads[@]}"; do
	run-rocksdb-fd $workload
	run-rocksdb $workload rocksdb-tiered
	run-rocksdb $workload prismdb
	run-rocksdb $workload SAS-Cache
	run-hotrap $workload hotrap
done

run-workload "u24685531"
run-workload "2-4-6-8"
run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-compaction

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	run-rocksdb $workload mutant
done

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	run-rocksdb $workload mutant "--run_70p_ops=10000"
done

hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB_200B"
	"ycsba_hotspot0.05_110GB_220GB_200B"
	"ycsbc_hotspot0.05_110GB_220GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_220GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_220GB_200B"
	"ycsba_uniform_110GB_220GB_200B"
	"ycsbc_uniform_110GB_220GB_200B"
)

for workload in "${hotspot_workloads[@]}"; do
	run-hotrap $workload hotrap
	run-rocksdb-fd $workload
done
for workload in "${uniform_workloads[@]}"; do
	run-hotrap $workload hotrap
	run-rocksdb $workload rocksdb-tiered
done
