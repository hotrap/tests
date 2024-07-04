workloads=(
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
function run-secondary-cache {
	../helper/checkout-secondary-cache
	DIR=../../data/$1/secondary-cache
	echo Result directory: $DIR
	./test-secondary-cache-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-sas-cache {
	../helper/checkout-SAS-Cache
	DIR=../../data/$1/SAS-Cache
	echo Result directory: $DIR
	./test-SAS-Cache-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-110GB.sh ../config/$1 $DIR 10GB
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR "$3"
	../helper/hotrap-plot.sh $DIR
}

workload="u155243"
../helper/checkout-promote-stably-hot
DIR=../../data/$workload/promote-stably-hot
echo Result directory: $DIR
./test-hotrap-110GB-generic.sh $DIR "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--enable_fast_generator --workload=$workload --switches=0x1"
../helper/hotrap-plot.sh $DIR

workload="read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
run-rocksdb-fd $workload
run-secondary-cache $workload
run-rocksdb $workload rocksdb-fat
run-hotrap $workload promote-stably-hot "--load_phase_rate_limit=800000000"

for workload in "${workloads[@]}"; do
	run-rocksdb-fd $workload
	run-secondary-cache $workload
	run-sas-cache $workload
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload promote-stably-hot
done

run-hotrap "ycsbc_hotspotshifting0.05_110GB_220GB" promote-stably-hot
run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-compaction

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
	run-hotrap $workload promote-stably-hot
	run-rocksdb-fd $workload
done
for workload in "${uniform_workloads[@]}"; do
	run-hotrap $workload promote-stably-hot
	run-rocksdb $workload rocksdb-fat
done
