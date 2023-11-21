workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB"
)
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
	# Reserve 250MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.75GB 5.5GB
	../helper/hotrap-plot.sh $DIR
}
function run-rocksdb-sd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-sd
	echo Result directory: $DIR
	./test-rocksdb-sd-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run-hotrap $workload with-probation
	run-hotrap $workload viscnts-splay-rs
	run-hotrap $workload flush-stably-hot
	run-rocksdb $workload rocksdb-fat
	run-rocksdb-sd $workload
done
