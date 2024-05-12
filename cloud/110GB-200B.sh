if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_200B"
	"ycsba_hotspot0.05_110GB_200B"
	"ycsbc_hotspot0.05_110GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_200B"
	"ycsba_uniform_110GB_200B"
	"ycsbc_uniform_110GB_200B"
)

source common.sh

function run-rocksdb-fd {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-fd-110GB.sh ../config/$workload ../../data/$workload/$version --optimize_filters_for_hits"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-110GB.sh ../config/$workload ../../data/$workload/$version 10GB --optimize_filters_for_hits"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$workload ../../data/$workload/$version 5.5GB 1.65GB --optimize_filters_for_hits"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${hotspot_workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot
	cloud-run run-rocksdb-fd $workload rocksdb-fd
done
for workload in "${uniform_workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot
	cloud-run run-rocksdb $workload rocksdb-fat
done
wait
