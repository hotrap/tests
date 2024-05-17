hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB_200B"
	"ycsba_hotspot0.05_110GB_220GB_200B"
	"ycsbc_hotspot0.05_110GB_220GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_220GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_220GB_200B"
	"ycsba_uniform_110GB_220GB_200B"
	"ycsbc_uniform_110GB_220GB_200B"
)

function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR 5GB 1.5GB "--optimize_filters_for_hits --enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size"
	../helper/hotrap-plot.sh $DIR
}

for workload in "${hotspot_workloads[@]}"; do
	run-hotrap $workload promote-stably-hot
done
for workload in "${uniform_workloads[@]}"; do
	run-hotrap $workload promote-stably-hot
done
