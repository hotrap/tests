cd "$(dirname $0)"

workloads=(
	"workload_110GB_wr_hotspot0.05"
	"workload_110GB_wr_uniform"
	"workload_110GB_wr_zipfian"
	"workload_110GB_wh_hotspot0.05"
	"workload_110GB_wh_uniform"
	"workload_110GB_wh_zipfian"
	"workload_110GB_ycsba_hotspot0.05"
	"workload_110GB_ycsba_uniform"
	"workload_110GB_ycsba_zipfian"
	"workload_110GB_ycsbc_hotspot0.05"
	"workload_110GB_ycsbc_uniform"
	"workload_110GB_ycsbc_zipfian"
)

function run-prismdb {
	../helper/checkout-prismdb
	DIR=../../data/$1/prismdb
	echo Result directory: $DIR
	./test-prismdb-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}

function run-mutant {
	../helper/checkout-mutant
	DIR=../../data/$1/mutant
	echo Result directory: $DIR
	./test-mutant-110GB.sh ../config/$1 $DIR
	../helper/plot-prismdb-mutant.sh $DIR
}

for workload in "${workloads[@]}"; do
	run-prismdb $workload
	run-mutant $workload
done
