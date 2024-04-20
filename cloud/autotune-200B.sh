if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_165GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_165GB_200B"
	"ycsba_hotspot0.05_110GB_165GB_200B"
	"ycsbc_hotspot0.05_110GB_165GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_165GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_165GB_200B"
	"ycsba_uniform_110GB_165GB_200B"
	"ycsbc_uniform_110GB_165GB_200B"
)

source common.sh
check-workload-files "${hotspot_workloads[@]}"
check-workload-files "${uniform_workloads[@]}"

function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP promote-stably-hot
	# Reserve 1.65GB for VisCnts
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB-200B.sh ../config/$workload ../../data/$workload/$version 8.35GB 5.5GB 1.65GB \"--enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${hotspot_workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot-autotune
done
for workload in "${uniform_workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot-autotune
done
wait
