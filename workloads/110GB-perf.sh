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
function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR-load
	./test-rocksdb-110GB.sh ../config/$1 $DIR-load 10GB "--load"
	echo Result directory: $DIR-run
	./test-rocksdb-110GB-perf.sh ../config/$1 $DIR-perf-run 10GB
	../helper/rocksdb-plot.sh $DIR-perf-run
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR-load
	./test-hotrap-110GB.sh ../config/$1 $DIR-load 9.67GB 5.5GB 330MB "--load"
	echo Result directory: $DIR-run
	./test-hotrap-110GB-perf.sh ../config/$1 $DIR-perf-run 9.67GB 5.5GB 330MB
	../helper/hotrap-plot.sh $DIR-perf-run
}
for workload in "${workloads[@]}"; do
	run-rocksdb $workload rocksdb-fat
	run-hotrap $workload promote-stably-hot
done
