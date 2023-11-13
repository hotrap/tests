workloads=(
	"ycsba_hotspot0.01_110GB"
	"ycsbc_hotspot0.01_110GB"
	"ycsbd_hotspot0.01_110GB"
	"ycsbf_hotspot0.01_110GB"
	"read_0.5_insert_0.5_hotspot0.01_110GB"
)
function run_rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb
	echo Result directory: $DIR
	./test-rocksdb-all-in-sd-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload
done
