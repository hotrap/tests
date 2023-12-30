hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_200B"
	"ycsba_hotspot0.05_110GB_200B"
	"ycsbc_hotspot0.05_110GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_200B"
	"ycsba_uniform_110GB_200B"
	"ycsbc_uniform_110GB_200B"
)
function run-rocksdb-sd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-sd
	echo Result directory: $DIR
	./test-rocksdb-sd-110GB-200B.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-110GB-200B.sh ../config/$1 $DIR 10GB
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 1.65GB for VisCnts
	./test-hotrap-110GB-200B.sh ../config/$1 $DIR 8.35GB 5.5GB 1.65GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${hotspot_workloads[@]}"; do
	run-hotrap $workload promote-stably-hot
	run-rocksdb-sd $workload
done
for workload in "${uniform_workloads[@]}"; do
	run-hotrap $workload promote-stably-hot
	run-rocksdb $workload rocksdb-fat
done
