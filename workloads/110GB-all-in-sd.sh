workloads=(
	"read_0.5_insert_0.5_hotspot0.01_110GB"
	"ycsba_hotspot0.01_110GB"
	"ycsbc_hotspot0.01_110GB"
	"ycsbd_hotspot0.01_110GB"
	"ycsbf_hotspot0.01_110GB"
	"read_0.5_insert_0.5_uniform_110GB"
	"ycsba_uniform_110GB"
	"ycsbc_uniform_110GB"
	"ycsbd_uniform_110GB"
	"ycsbf_uniform_110GB"
	"read_0.5_insert_0.5_zipfian_110GB"
	"ycsba_zipfian_110GB"
	"ycsbc_zipfian_110GB"
	"ycsbd_zipfian_110GB"
	"ycsbf_zipfian_110GB"
)
function run_rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-sd
	echo Result directory: $DIR
	./test-rocksdb-all-in-sd-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload
done
