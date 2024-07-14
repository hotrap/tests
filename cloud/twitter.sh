if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

workloads=(
	"cluster01-4168x"
	"cluster02-283x"
	"cluster03-135x"
	"cluster04-3x"
	"cluster05"
	"cluster06-7x"
	"cluster07-12x"
	"cluster08-95x"
	"cluster09-113x"
	"cluster10"
	"cluster11-25x"
	"cluster12"
	"cluster13"
	"cluster14-3x"
	"cluster15"
	"cluster16-67x"
	"cluster17-80x"
	"cluster18-186x"
	"cluster19-3x"
	"cluster20-16x"
	"cluster21-3x"
	"cluster22-9x"
	"cluster23"
	"cluster24-11x"
	"cluster25-215x"
	"cluster26-8x"
	"cluster27-7x"
	"cluster28-17x"
	"cluster29"
	"cluster30-10x"
	"cluster31-2x"
	"cluster32"
	"cluster33-5x"
	"cluster34-9x"
	"cluster35"
	"cluster36-18x"
	"cluster37"
	"cluster38"
	"cluster39"
	"cluster40-5x"
	"cluster41-6x"
	"cluster42-15x"
	"cluster43-4x"
	"cluster44-40x"
	"cluster45-18x"
	"cluster46"
	"cluster47-74x"
	"cluster48-5x"
	"cluster49-17x"
	"cluster50"
	"cluster51-175x"
	"cluster52-3x"
	"cluster53-12x"
	"cluster54-11x"
)
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

source common.sh

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

function run-rocksdb-fd {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb-fd-110GB-replay.sh $prefix ../../data/$workload/$version \"--enable_fast_process\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-$version-110GB-replay.sh $prefix ../../data/$workload/$version \"--enable_fast_process\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	upload-trace
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB-replay.sh $prefix ../../data/$workload/$version \"--enable_fast_process\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

num=${#workloads[@]}
max_concurrent=10
i=0
running=0
while [ $i -lt $num ]; do
	workload="${workloads[$i]}"
	cloud-run run-rocksdb-fd $workload rocksdb-fd
	cloud-run run-rocksdb $workload rocksdb-fat
	cloud-run run-rocksdb $workload SAS-Cache
	cloud-run run-rocksdb $workload mutant
	cloud-run run-rocksdb $workload prismdb
	cloud-run run-hotrap $workload promote-stably-hot
	i=$(($i + 1))
	running=$(($running + 1))
	if [ $running -eq $max_concurrent ]; then
		wait -n
		wait -n
		wait -n
		wait -n
		wait -n
		wait -n
		running=$(($running - 1))
	fi
done
wait
