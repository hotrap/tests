workloads=(
	"read_0.5_insert_0.5_hotspot0.05_11GB"
	"ycsba_hotspot0.05_11GB"
	"ycsbc_hotspot0.05_11GB"
	"ycsbd_hotspot0.05_11GB"
	"ycsbf_hotspot0.05_11GB"
	"read_0.5_insert_0.5_uniform_11GB"
	"ycsba_uniform_11GB"
	"ycsbc_uniform_11GB"
	"ycsbd_uniform_11GB"
	"ycsbf_uniform_11GB"
	"read_0.5_insert_0.5_zipfian_11GB"
	"ycsba_zipfian_11GB"
	"ycsbc_zipfian_11GB"
	"ycsbd_zipfian_11GB"
	"ycsbf_zipfian_11GB"
)
function run-rocksdb-sd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-sd
	echo Result directory: $DIR
	./test-rocksdb-sd-11GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-secondary-cache {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-secondary-cache-11GB.sh ../config/$1 $DIR 1GB 550MB
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-11GB.sh ../config/$1 $DIR 1GB
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 25MB for VisCnts
	./test-hotrap-11GB.sh ../config/$1 $DIR 0.975GB 550MB
	../helper/hotrap-plot-11GB.sh $DIR
}
for workload in "${workloads[@]}"; do
	run-rocksdb-sd $workload
	run-secondary-cache $workload secondary-cache
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload flush-stably-hot
	run-hotrap $workload with-probation
	run_hotrap $workload viscnts-splay-rs
done
