if [[ $# < 2 || $# > 3 ]]; then
	echo Usage: $0 config-file output-dir [instance-name-prefix]
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
if [ $3 ]; then
	instance_name_prefix=$3
else
	instance_name_prefix=$(cat $config_file | jq -er ".instance_name_prefix")
	if [ $? -ne 0 ]; then
		instance_name_prefix=hotrap-auto-
	fi
fi
cd $(dirname $0)

hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_200B"
	"ycsba_hotspot0.05_110GB_200B"
	"ycsbc_hotspot0.05_110GB_200B"
	"ycsbd_hotspot0.05_110GB_200B"
	"ycsbf_hotspot0.05_110GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_200B"
	"ycsba_uniform_110GB_200B"
	"ycsbc_uniform_110GB_200B"
	"ycsbd_uniform_110GB_200B"
	"ycsbf_uniform_110GB_200B"
)

source common.sh

for workload in "${workloads[@]}"; do
	if [ ! -f ../config/$workload ]; then
		echo $workload does not exists!
		exit 1
	fi
done

function run-rocksdb-sd {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $IP
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-sd-110GB-200B.sh ../config/$workload ../../data/$workload/$version"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $IP
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-110GB-200B.sh ../config/$workload ../../data/$workload/$version 10GB"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $IP $version
	# Reserve 1.65GB for VisCnts
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB-200B.sh ../config/$workload ../../data/$workload/$version 8.35GB 5.5GB 1.65GB"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${hotspot_workloads[@]}"; do
	aliyun-run run-hotrap $workload flush-stably-hot
	aliyun-run run-rocksdb-sd $workload rocksdb-sd
done
for workload in "${uniform_workloads[@]}"; do
	aliyun-run run-hotrap $workload flush-stably-hot
	aliyun-run run-rocksdb $workload rocksdb-fat
done
wait
