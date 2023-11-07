workloads=(
	"ycsbc_uniform_110GB"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR 10GB 1.1GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-accessed
done
