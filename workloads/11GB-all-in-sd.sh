workloads=(
	"ycsba_hotspot0.01_11GB"
	"ycsbb_hotspot0.01_11GB"
	"ycsbc_hotspot0.01_11GB"
	"ycsbd_hotspot0.01_11GB"
	"ycsbf_hotspot0.01_11GB"
	"read_0.5_insert_0.5_hotspot0.01_11GB"
)
function run_rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb
	echo Result directory: $DIR
	./test-rocksdb-all-in-sd-11GB.sh ../config/$1 $DIR 1GB
	../helper/rocksdb-plot-11GB.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload
done
