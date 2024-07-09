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

function run {
	if [ -f ../config/$1_$2 ]; then
		workload_file=$1_$2
	else
		workload_file=$1
	fi
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-$2-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}

for workload in "${workloads[@]}"; do
	run $workload
	run $workload
done
