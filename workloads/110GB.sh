workloads=(
	"ycsba_hotspot0.01_110GB"
	"ycsbc_hotspot0.01_110GB"
	"ycsbc_uniform_110GB"
	"ycsbc_zipfian_110GB"
	"ycsbd_hotspot0.01_110GB"
	"ycsbf_hotspot0.01_110GB"
	"read_0.5_insert_0.5_hotspot0.01_110GB"
	"read_0.5_insert_0.5_uniform_110GB"
	"read_0.5_insert_0.5_zipfian_110GB"
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
	# Reserve 250MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.75GB 1.1GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-stably-hot
	run_rocksdb $workload rocksdb-fat
done
