if [[ $# != 3 ]]; then
	echo Usage: $0 config-file output-dir max-running-instances
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
max_running_instances=$3
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

. ./common.sh

function upload-trace {
	if [ -f ../../upload-trace ]; then
		../../upload-trace $user $IP $workload
	else
		ssh $user@$IP "mkdir -p twitter/processed"
		rsync -pt --partial -e ssh ../../twitter/processed/{$workload-*.zst,$workload.json} $user@$IP:~/twitter/processed/
		ssh $user@$IP "unzstd twitter/processed/$workload-*.zst"
	fi
	prefix=../../twitter/processed/$workload
}

function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $user $IP
	upload-trace
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-$version-110GB-replay.sh $prefix ../../data/$workload/$version \"--enable_fast_process\" && ../helper/rocksdb-plot.sh ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
}
function run-version {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $user $IP
	upload-trace
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-$version-110GB-replay.sh $prefix ../../data/$workload/$version \"--enable_fast_process\" && ../helper/rocksdb-plot.sh ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	upload-trace
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-hotrap-110GB-replay.sh $prefix ../../data/$workload/$version \"--enable_fast_process\" && ../helper/hotrap-plot.sh ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
}

function check-trace {
	for workload in "${workloads[@]}"; do
		trace_dir=../../twitter/processed
		if [ ! -f $trace_dir/$workload-load.zst ]; then
			echo $workload-load.zst does not exist
			exit 1
		fi
		if [ ! -f $trace_dir/$workload-run.zst ]; then
			echo $workload-run.zst does not exist
			exit 1
		fi
	done
}

workloads=(
	"cluster02-283x"
	"cluster11-25x"
	"cluster15"
	"cluster16-67x"
	"cluster17-80x"
	"cluster18-186x"
	"cluster19-3x"
	"cluster22-9x"
	"cluster23"
	"cluster29"
	"cluster46"
	"cluster48-5x"
	"cluster51-175x"
	"cluster53-12x"
)
check-trace
for workload in "${workloads[@]}"; do
	cloud-run machine-config/110GB.json run-rocksdb $workload rocksdb-tiered
	cloud-run machine-config/110GB.json run-hotrap $workload hotrap
done

workloads=(
	"cluster11-25x"
	"cluster15"
	"cluster17-80x"
	"cluster19-3x"
	"cluster29"
	"cluster53-12x"
)
check-trace
for workload in "${workloads[@]}"; do
	cloud-run machine-config/110GB.json run-rocksdb $workload rocksdb-fd
	cloud-run machine-config/110GB.json run-version $workload SAS-Cache
	cloud-run machine-config/110GB.json run-version $workload prismdb
	cloud-run machine-config/110GB.json run-version $workload cachelib
done
wait
