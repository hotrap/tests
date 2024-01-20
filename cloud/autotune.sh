if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_165GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_165GB"
	"ycsba_hotspot0.05_110GB_165GB"
	"ycsbc_hotspot0.05_110GB_165GB"
	"read_0.5_insert_0.5_zipfian_110GB_165GB"
	"read_0.75_insert_0.25_zipfian_110GB_165GB"
	"ycsba_zipfian_110GB_165GB"
	"ycsbc_zipfian_110GB_165GB"
	"read_0.5_insert_0.5_uniform_110GB_165GB"
	"read_0.75_insert_0.25_uniform_110GB_165GB"
	"ycsba_uniform_110GB_165GB"
	"ycsbc_uniform_110GB_165GB"
)

source common.sh

function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP promote-stably-hot
	# Reserve 330MB for VisCnts
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$workload ../../data/$workload/$version 9.67GB 5.5GB 330MB \"--enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size\""
	rsync -zPrt -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot-autotune
done
wait
