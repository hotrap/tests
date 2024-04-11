workloads=(
	"cluster29"
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
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	# Reserve 330MB for VisCnts
	./test-hotrap-replay-110GB.sh $prefix-load $prefix-run $DIR 9.67GB 5.5GB 330MB
	../helper/hotrap-plot.sh $DIR
}

for workload in "${workloads[@]}"; do
	run-rocksdb-fd $workload
	run-hotrap $workload promote-stably-hot
	run-secondary-cache $workload
done
