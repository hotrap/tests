workloads=(
	"ycsbc_hotspot0.1_20GB_100B"
	"ycsbc_hotspot0.1_20GB"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-20GB.sh ../config/$1 $DIR 5GB
	../helper/rocksdb-plot.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-20GB.sh ../config/$1 $DIR 5GB 2GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-stably-hot
done
