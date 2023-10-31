workloads=(
	"ycsbc_hotspot0.1_20GB_100B"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-20GB.sh ../config/$1 $DIR 5GB 2GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-stably-hot
done
