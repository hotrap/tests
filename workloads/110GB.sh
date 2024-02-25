workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB"
	"ycsba_hotspot0.05_110GB"
	"ycsbc_hotspot0.05_110GB"
	"read_0.5_insert_0.5_uniform_110GB"
	"read_0.75_insert_0.25_uniform_110GB"
	"ycsba_uniform_110GB"
	"ycsbc_uniform_110GB"
	"read_0.5_insert_0.5_zipfian_110GB"
	"read_0.75_insert_0.25_zipfian_110GB"
	"ycsba_zipfian_110GB"
	"ycsbc_zipfian_110GB"
)
function run-rocksdb-fd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-fd
	echo Result directory: $DIR
	./test-rocksdb-fd-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-secondary-cache {
	../helper/checkout-secondary-cache
	DIR=../../data/$1/secondary-cache
	echo Result directory: $DIR
	./test-secondary-cache-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
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
	# Reserve 330MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.67GB 5.5GB 330MB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run-rocksdb-fd $workload
	run-secondary-cache $workload
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload promote-stably-hot
done
run-hotrap "ycsbc_hotspotshifting0.05_110GB" promote-stably-hot
run-hotrap "ycsbc_uniform_110GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB" no-promote-by-compaction
