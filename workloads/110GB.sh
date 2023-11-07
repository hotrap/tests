workloads=(
	"ycsbc_hotspot0.01_110GB"
	"ycsbc_hotspotshifting0.01_110GB"
	"ycsbc_uniform_110GB"
	"ycsbc_zipfian_110GB"
	"hotspot0.01_110GB_read_0.5_insert_0.5"
	"latest_110GB_read_0.5_insert_0.5"
	"uniform_110GB_read_0.5_insert_0.5"
	"zipfian_110GB_read_0.5_insert_0.5"
	"ycsbc_hotspot0.01_110GB_200B"
	"hotspot0.01_110GB_200B_read_0.5_insert_0.5"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-110GB.sh ../config/$1 $DIR 10GB
	../helper/rocksdb-plot.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR 10GB 1.1GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-stably-hot
	run_rocksdb $workload rocksdb-fat
done
