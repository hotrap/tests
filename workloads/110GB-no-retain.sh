workloads=(
	"read_0.5_insert_0.5_hotspot0.01_110GB"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 250MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.75GB 1.1GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload no-retain
done
