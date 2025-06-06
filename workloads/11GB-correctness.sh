workloads=(
	"read_0.5_insert_0.5_hotspot0.05_11GB"
	"read_0.75_insert_0.25_hotspot0.05_11GB"
	"ycsba_hotspot0.05_11GB"
	"ycsbc_hotspot0.05_11GB"
	"read_0.5_insert_0.5_uniform_11GB"
	"read_0.75_insert_0.25_uniform_11GB"
	"ycsba_uniform_11GB"
	"ycsbc_uniform_11GB"
	"read_0.5_insert_0.5_zipfian_11GB"
	"read_0.75_insert_0.25_zipfian_11GB"
	"ycsba_zipfian_11GB"
	"ycsbc_zipfian_11GB"
)
function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	prefix=../../YCSB-traces/$1
	./test-$2-replay.sh 11GB $prefix $DIR "--export_ans_xxh64 $3"
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	prefix=../../YCSB-traces/$1
	./test-hotrap-11GB-replay.sh $prefix $DIR "--export_ans_xxh64 $3"
	../helper/hotrap-plot-11GB.sh $DIR
	../tools/check-ans.sh ../../data/$1/rocksdb-fd-correctness/ $DIR/
}
for workload in "${workloads[@]}"; do
	../helper/gen-ycsb-trace.sh ../config/$workload
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
done
run-hotrap "ycsbc_uniform_11GB" promote-accessed
