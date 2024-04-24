if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

workloads=(
	"cluster03-138x"
	"cluster04-3x"
	"cluster05"
	"cluster06-7x"
	"cluster08-95x"
	"cluster10"
	"cluster11-26x"
	"cluster12"
	"cluster13"
	"cluster14-3x"
	"cluster15"
	"cluster16-68x"
	"cluster17-80x"
	"cluster19-3x"
	"cluster29"
	"cluster46"
	"cluster48-5x"
)
for workload in "${workloads[@]}"; do
	trace_dir=../../twitter/processed
	if [ ! -f $trace_dir/$workload-load ]; then
		echo $workload-load does not exist
		exit 1
	fi
	if [ ! -f $trace_dir/$workload-run ]; then
		echo $workload-run does not exist
		exit 1
	fi
done

source common.sh

function upload-trace {
	if [ -f ../../upload-trace ]; then
		../../upload-trace $user $IP $workload
	else
		ssh $user@$IP "mkdir -p twitter/processed"
		rsync -zpt --partial -e ssh ../../twitter/processed/$workload-*.zst $user@$IP:~/twitter/processed/
		ssh $user@$IP "unzstd twitter/processed/$workload-*.zst"
	fi
	prefix=../../twitter/processed/$workload
}

function run-rocksdb-fd {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-fd-replay-110GB.sh $prefix-load $prefix-run ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-replay-110GB.sh $prefix-load $prefix-run ../../data/$workload/$version 10GB"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-secondary-cache {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-secondary-cache $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-secondary-cache-replay-110GB.sh $prefix-load $prefix-run ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-hotrap $user $IP $version
	# Reserve 330MB for VisCnts
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-replay-110GB.sh $prefix-load $prefix-run ../../data/$workload/$version 9.67GB 5.5GB 330MB"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb-fd $workload rocksdb-fd
	cloud-run run-rocksdb $workload rocksdb-fat
	cloud-run run-secondary-cache $workload secondary-cache
	cloud-run run-hotrap $workload promote-stably-hot
done
wait
