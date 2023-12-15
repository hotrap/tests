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
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-sd-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $IP
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-110GB.sh ../config/$workload ../../data/$workload/$version 10GB"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-secondary-cache {
	workload=$1
	version=$2
	IP=$3
	./checkout-secondary-cache $IP
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-secondary-cache-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $IP $version
	# Reserve 330MB for VisCnts
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$workload ../../data/$workload/$version 9.67GB 5.5GB 330MB"
	rsync -zPrt -e ssh root@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${workloads[@]}"; do
	aliyun-run run-rocksdb-sd $workload rocksdb-sd
	aliyun-run run-rocksdb $workload rocksdb-fat
	aliyun-run run-secondary-cache $workload secondary-cache
	aliyun-run run-hotrap $workload flush-stably-hot
done
aliyun-run run-hotrap "ycsbc_hotspotshifting0.05_110GB" flush-stably-hot
aliyun-run run-hotrap "ycsbc_uniform_110GB" flush-accessed
aliyun-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB" no-retain
aliyun-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB" no-promote-by-compaction
wait
