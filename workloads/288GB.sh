workloads=(
	"latest_288GB_read_0.5_insert_0.5"
	"hotspot0.01_288GB_read_0.5_insert_0.5"
	"uniform_288GB_read_0.5_insert_0.5"
	"zipfian_288GB_read_0.5_insert_0.5"
	"ycsbc_hotspot0.01_288GB"
	"ycsbc_hotspotshifting0.01_288GB"
	"ycsbc_uniform_288GB"
	"ycsbc_zipfian_288GB"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb.sh ../config/$1 $DIR 32GB
	../helper/rocksdb-plot.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap.sh ../config/$1 $DIR 32GB 2.88GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-accessed
	run_hotrap $workload flush-stably-hot
done
