workloads=(
	"ycsbc_hotspot0.01_11GB"
	"ycsbc_hotspotshifting0.01_11GB"
	"ycsbc_uniform_11GB"
	"ycsbc_zipfian_11GB"
	"hotspot0.01_11GB_read_0.5_insert_0.5"
	"latest_11GB_read_0.5_insert_0.5"
	"uniform_11GB_read_0.5_insert_0.5"
	"zipfian_11GB_read_0.5_insert_0.5"
	"ycsbc_hotspot0.01_11GB_200B"
	"hotspot0.01_11GB_200B_read_0.5_insert_0.5"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-11GB.sh ../config/$1 $DIR 1GB
	../helper/rocksdb-plot.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-11GB.sh ../config/$1 $DIR 1GB 110MB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-stably-hot
done
