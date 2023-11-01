workloads=(
	"ycsbc_hotspot0.05_144GB_100B"
	"hotspot0.05_144GB_100B_read_0.5_insert_0.5"
)
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-144GB.sh ../config/$1 $DIR 16GB 7.2GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-stably-hot
	run_hotrap $workload viscnts-splay-rs
done
