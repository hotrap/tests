workloads=(
	"read_0.5_insert_0.5_hotspot0.01_11GB"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 25MB for VisCnts
	./test-hotrap-11GB.sh ../config/$1 $DIR 0.975GB 110MB
	../helper/hotrap-plot-11GB.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload no-retain
done
