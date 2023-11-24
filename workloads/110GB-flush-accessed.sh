workloads=(
	"ycsbc_uniform_110GB"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 250MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.75GB 5.5GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-accessed
done
