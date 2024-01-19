workloads=(
	"ycsbc_hotspot0.05_110GB_165GB"
)
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2-autotune
	echo Result directory: $DIR
	# Reserve 330MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR 9.67GB 5.5GB 330MB "--enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size"
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run-hotrap $workload promote-stably-hot
done
