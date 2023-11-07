workloads=(
	"hotspot0.01_110GB_read_0.5_insert_0.5"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR 10GB 1.1GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload no-retain
done
