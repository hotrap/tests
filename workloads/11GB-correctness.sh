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
function run-rocksdb-fd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-fd-correctness
	echo Result directory: $DIR
	./test-rocksdb-fd-11GB-replay.sh $1 $DIR
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	./test-hotrap-11GB-replay.sh $1 $DIR
	../helper/hotrap-plot-11GB.sh $DIR
	../helper/check-ans.sh ../../data/$1/rocksdb-fd-correctness/ $DIR/
}
for workload in "${workloads[@]}"; do
	../helper/gen-ycsb-trace.sh ../config/$workload
	run-rocksdb-fd $workload
	run-hotrap $workload promote-stably-hot
	run-hotrap $workload viscnts-splay-rs
done
run-hotrap "ycsbc_uniform_11GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" no-promote-by-compaction
