function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-$2-110GB-replay.sh $prefix $DIR "--enable_fast_process"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-hotrap-110GB-replay.sh $prefix $DIR "--enable_fast_process"
	../helper/hotrap-plot.sh $DIR
}
function run-version {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-$2-110GB-replay.sh $prefix $DIR "--enable_fast_process"
	../helper/rocksdb-plot.sh $DIR
}

workloads=(
	"cluster02-283x"
	"cluster11-25x"
	"cluster15"
	"cluster16-67x"
	"cluster17-80x"
	"cluster18-186x"
	"cluster19-3x"
	"cluster22-9x"
	"cluster23"
	"cluster29"
	"cluster46"
	"cluster48-5x"
	"cluster51-175x"
	"cluster53-12x"
)
for workload in "${workloads[@]}"; do
	../helper/unzstd-processed.sh $workload
	run-hotrap $workload hotrap
	run-rocksdb $workload rocksdb-tiered
	../helper/delete-uncompressed.sh $workload
done

workloads=(
	"cluster11-25x"
	"cluster15"
	"cluster17-80x"
	"cluster19-3x"
	"cluster29"
	"cluster53-12x"
)
for workload in "${workloads[@]}"; do
	../helper/unzstd-processed.sh $workload
	run-rocksdb $workload rocksdb-fd
	run-version $workload cachelib
	run-version $workload SAS-Cache
	run-version $workload prismdb
	../helper/delete-uncompressed.sh $workload
done
