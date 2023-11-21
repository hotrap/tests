workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_200B"
	"ycsba_hotspot0.05_110GB_200B"
	"ycsbc_hotspot0.05_110GB_200B"
	"ycsbd_hotspot0.05_110GB_200B"
	"ycsbf_hotspot0.05_110GB_200B"
	"read_0.5_insert_0.5_uniform_110GB_200B"
	"ycsba_uniform_110GB_200B"
	"ycsbc_uniform_110GB_200B"
	"ycsbd_uniform_110GB_200B"
	"ycsbf_uniform_110GB_200B"
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
	# Reserve 1.5GB for viscnts-lsm
	./test-hotrap-110GB.sh ../config/$1 $DIR 8.5GB 5.5GB
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
	run-hotrap $workload flush-stably-hot
	run-rocksdb $workload rocksdb-fat
	run-rocksdb-sd $workload
done
