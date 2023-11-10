workloads=(
	"ycsbc_hotspot0.05_110GB_200B"
	"read_0.5_insert_0.5_hotspot0.05_110GB_200B"
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
	# Reserve 1.5GB for viscnts-lsm
	./test-hotrap-110GB.sh ../config/$1 $DIR 8.5GB 5.5GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-stably-hot
	run_rocksdb $workload rocksdb-fat
done