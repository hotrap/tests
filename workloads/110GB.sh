workloads=(
	"ycsba_hotspot0.01_110GB"
	"ycsbc_hotspot0.01_110GB"
	"ycsbd_hotspot0.01_110GB"
	"ycsbf_hotspot0.01_110GB"
	"read_0.5_insert_0.5_hotspot0.01_110GB"
	"ycsba_uniform_110GB"
	"ycsbc_uniform_110GB"
	"ycsbd_uniform_110GB"
	"ycsbf_uniform_110GB"
	"read_0.5_insert_0.5_uniform_110GB"
	"ycsba_zipfian_110GB"
	"ycsbc_zipfian_110GB"
	"ycsbd_zipfian_110GB"
	"ycsbf_zipfian_110GB"
	"read_0.5_insert_0.5_zipfian_110GB"
	"ycsbc_hotspotshifting0.01_110GB"
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
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.75GB 1.1GB
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
