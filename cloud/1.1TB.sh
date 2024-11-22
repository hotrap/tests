if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

. ./common.sh

function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-$version-1.1TB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-hotrap-1.1TB.sh ../config/$workload ../../data/$workload/$version \"${@:4}\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_1.1TB_2.2TB"
	"read_0.75_insert_0.25_hotspot0.05_1.1TB_2.2TB"
	"ycsba_hotspot0.05_1.1TB_2.2TB"
	"ycsbc_hotspot0.05_1.1TB_2.2TB"
	"ycsbc_zipfian_1.1TB"
)
check-workload-files "${workloads[@]}"

for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb $workload rocksdb-tiered
	cloud-run run-hotrap $workload hotrap
done
wait
