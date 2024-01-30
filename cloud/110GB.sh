if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB"
	"ycsba_hotspot0.05_110GB"
	"ycsbc_hotspot0.05_110GB"
	"read_0.5_insert_0.5_zipfian_110GB"
	"read_0.75_insert_0.25_zipfian_110GB"
	"ycsba_zipfian_110GB"
	"ycsbc_zipfian_110GB"
	"read_0.5_insert_0.5_uniform_110GB"
	"read_0.75_insert_0.25_uniform_110GB"
	"ycsba_uniform_110GB"
	"ycsbc_uniform_110GB"
)

source common.sh

function run-rocksdb-sd {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-sd-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zPrt -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-110GB.sh ../config/$workload ../../data/$workload/$version 10GB"
	rsync -zPrt -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-secondary-cache {
	workload=$1
	version=$2
	IP=$3
	./checkout-secondary-cache $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-secondary-cache-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zPrt -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	# Reserve 330MB for VisCnts
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$workload ../../data/$workload/$version 9.67GB 5.5GB 330MB"
	rsync -zPrt -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb-sd $workload rocksdb-sd
	cloud-run run-rocksdb $workload rocksdb-fat
	cloud-run run-secondary-cache $workload secondary-cache
	cloud-run run-hotrap $workload promote-stably-hot
done
cloud-run run-hotrap "ycsbc_hotspotshifting0.05_110GB_150GB" promote-stably-hot
cloud-run run-hotrap "ycsbc_uniform_110GB" promote-accessed
cloud-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB" no-retain
cloud-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB" no-promote-by-compaction
wait
