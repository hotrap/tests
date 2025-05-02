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
function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-$2-11GB.sh ../config/$1 $DIR
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
	run-rocksdb $workload rocksdb-fd
	run-rocksdb $workload rocksdb-tiered
	run-hotrap $workload hotrap
done
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" hotrap
run-hotrap "ycsbc_uniform_11GB" promote-accessed

run-rocksdb "ycsbc_hotspot0.05_11GB_200B" rocksdb-fd
