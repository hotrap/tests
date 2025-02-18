function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-$2-1.1TB.sh ../config/$1 $DIR "$3"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-1.1TB.sh ../config/$1 $DIR "$3"
	../helper/hotrap-plot.sh $DIR
}

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_1.1TB"
	"read_0.75_insert_0.25_hotspot0.05_1.1TB"
	"ycsba_hotspot0.05_1.1TB"
	"ycsbc_hotspot0.05_1.1TB"
	"read_0.5_insert_0.5_zipfian_1.1TB"
	"read_0.75_insert_0.25_zipfian_1.1TB"
	"ycsba_zipfian_1.1TB"
	"ycsbc_zipfian_1.1TB"
	"read_0.5_insert_0.5_uniform_1.1TB"
	"read_0.75_insert_0.25_uniform_1.1TB"
	"ycsba_uniform_1.1TB"
	"ycsbc_uniform_1.1TB"
)
for workload in "${workloads[@]}"; do
	run-rocksdb $workload rocksdb-fd
	run-rocksdb $workload rocksdb-tiered
done

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_1.1TB_2.2TB"
	"read_0.75_insert_0.25_hotspot0.05_1.1TB_2.2TB"
	"ycsba_hotspot0.05_1.1TB_2.2TB"
	"ycsbc_hotspot0.05_1.1TB_2.2TB"
	"read_0.5_insert_0.5_zipfian_1.1TB_2.2TB"
	"read_0.75_insert_0.25_zipfian_1.1TB_2.2TB"
	"ycsba_zipfian_1.1TB_2.2TB"
	"ycsbc_zipfian_1.1TB_2.2TB"
	"read_0.5_insert_0.5_uniform_1.1TB_2.2TB"
	"read_0.75_insert_0.25_uniform_1.1TB_2.2TB"
	"ycsba_uniform_1.1TB_2.2TB"
	"ycsbc_uniform_1.1TB_2.2TB"
)
for workload in "${workloads[@]}"; do
	run-hotrap $workload hotrap
done
