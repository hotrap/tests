workloads=(
	"read_0.5_insert_0.5_hotspot0.05_11GB"
	"ycsba_hotspot0.05_11GB"
	"ycsbc_hotspot0.05_11GB"
	"read_0.5_insert_0.5_uniform_11GB"
	"ycsba_uniform_11GB"
	"ycsbc_uniform_11GB"
	"read_0.5_insert_0.5_zipfian_11GB"
	"ycsba_zipfian_11GB"
	"ycsbc_zipfian_11GB"
)
function run-rocksdb-fd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-fd
	echo Result directory: $DIR
	./test-rocksdb-fd-11GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-11GB.sh ../config/$1 $DIR 1GB
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-secondary-cache {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-secondary-cache-11GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 33MB for RALT
	./test-hotrap-11GB.sh ../config/$1 $DIR
	../helper/hotrap-plot-11GB.sh $DIR
}
for workload in "${workloads[@]}"; do
	run-rocksdb-fd $workload
	run-secondary-cache $workload secondary-cache
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload hotrap
done
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" hotrap
run-hotrap "ycsbc_uniform_11GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" no-promote-by-compaction
