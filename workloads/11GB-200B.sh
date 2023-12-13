workloads=(
	"read_0.5_insert_0.5_hotspot0.05_11GB_200B"
	"ycsbc_hotspot0.05_11GB_200B"
)
function run-rocksdb-sd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-sd
	echo Result directory: $DIR
	./test-rocksdb-sd-11GB-200B.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-11GB-200B.sh ../config/$1 $DIR 1GB
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 150MB for viscnts-lsm
	./test-hotrap-11GB-200B.sh ../config/$1 $DIR 850MB 550MB 150MB
	../helper/hotrap-plot-11GB.sh $DIR
}
for workload in "${workloads[@]}"; do
	run-rocksdb-sd $workload
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload flush-stably-hot
done
