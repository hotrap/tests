function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2-perf
	echo Result directory: $DIR
	./test-$2-110GB-perf.sh ../config/$1 $DIR "$3"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2-perf
	echo Result directory: $DIR
	./test-hotrap-110GB-perf.sh ../config/$1 $DIR "$3"
	../helper/hotrap-plot.sh $DIR
}

hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB_200B"
)

for workload in "${hotspot_workloads[@]}"; do
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
done
