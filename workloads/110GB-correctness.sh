workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)
function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	prefix=../../YCSB-traces/$1
	./test-$2-110GB-replay.sh $prefix $DIR "--export_ans_xxh64 $3"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	prefix=../../YCSB-traces/$1
	./test-hotrap-110GB-replay.sh $prefix $DIR "--export_ans_xxh64 $3"
	../helper/hotrap-plot.sh $DIR
	../tools/check-ans.sh ../../data/$1/rocksdb-fd-correctness/ $DIR/
}

for workload in "${workloads[@]}"; do
	../helper/gen-ycsb-trace.sh ../config/$workload
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
done

run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-compaction

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB_200B"
	"ycsba_hotspot0.05_110GB_220GB_200B"
	"ycsbc_hotspot0.05_110GB_220GB_200B"
	"read_0.5_insert_0.5_uniform_110GB_220GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_220GB_200B"
	"ycsba_uniform_110GB_220GB_200B"
	"ycsbc_uniform_110GB_220GB_200B"
)

for workload in "${workloads[@]}"; do
	../helper/gen-ycsb-trace.sh ../config/$workload
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
done
