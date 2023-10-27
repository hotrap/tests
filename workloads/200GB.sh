workloads=(
	"latest_200GB_read_0.5_insert_0.5"
	"hotspot0.1_200GB_read_0.5_insert_0.5"
	"hotspot0.01_200GB_read_0.5_insert_0.5"
	"uniform_200GB_read_0.5_insert_0.5"
	"zipfian_200GB_read_0.5_insert_0.5"
	"ycsbc_hotspot0.1_200GB"
	"ycsbc_hotspotshifting0.1_200GB"
	"ycsbc_uniform_200GB"
	"ycsbc_zipfian_200GB"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb.sh ../config/$1 $DIR 50GB
	../helper/rocksdb-plot.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap.sh ../config/$1 $DIR 50GB 20GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-accessed
	run_hotrap $workload flush-stably-hot
done
