workloads=(
	"cluster05"
	"cluster07-12x"
	"cluster09-118x"
	"cluster10"
	"cluster12"
	"cluster13"
	"cluster15"
	"cluster17-80x"
	"cluster18-197x"
	"cluster20-16x"
	"cluster21-3x"
	"cluster22-9x"
	"cluster23"
	"cluster24-11x"
	"cluster25-223x"
	"cluster26-8x"
	"cluster29"
	"cluster52-3x"
)
function run-rocksdb-fd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-fd
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-rocksdb-fd-replay-110GB.sh $prefix-load $prefix-run $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-secondary-cache {
	../helper/checkout-secondary-cache
	DIR=../../data/$1/secondary-cache
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-secondary-cache-replay-110GB.sh $prefix-load $prefix-run $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-rocksdb-replay-110GB.sh $prefix-load $prefix-run $DIR 10GB
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	# Reserve 330MB for VisCnts
	./test-hotrap-replay-110GB.sh $prefix-load $prefix-run $DIR 9.67GB 5.5GB 330MB "--enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size"
	../helper/hotrap-plot.sh $DIR
}

for workload in "${workloads[@]}"; do
	run-rocksdb-fd $workload
	run-secondary-cache $workload
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload promote-stably-hot
done
