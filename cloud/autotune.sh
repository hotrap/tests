if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)

source common.sh

function run-rocksdb-fd {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-fd-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-110GB.sh ../config/$workload ../../data/$workload/$version 10GB"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-secondary-cache {
	workload=$1
	version=$2
	IP=$3
	./checkout-secondary-cache $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-secondary-cache-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$workload ../../data/$workload/$version 5.5GB 330MB \"--enable_dynamic_vc_param_in_lsm --enable_dynamic_only_vc_phy_size\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb-fd $workload rocksdb-fd
	cloud-run run-rocksdb $workload rocksdb-fat
	cloud-run run-secondary-cache $workload secondary-cache
	cloud-run run-hotrap $workload promote-stably-hot
done
cloud-run run-hotrap "ycsbc_hotspotshifting0.05_110GB_220GB" promote-stably-hot
cloud-run run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
cloud-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-retain
cloud-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-compaction
wait
