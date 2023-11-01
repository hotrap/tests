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

source common.sh

workloads=(
	"ycsbc_hotspot0.01_200GB"
	"ycsbc_hotspotshifting0.01_200GB"
	"ycsbc_uniform_200GB"
	"ycsbc_zipfian_200GB"
)
function run_rocksdb_1 {
	setup $1 $2 $3
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-rocksdb.sh ../config/$1 ../../data/$1/$2 50GB"
	rsync -zPrt -e ssh root@$IP:~/data/$1 $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$1/$2
	./delete.py $config_file $instance_id
}
function run_hotrap_1 {
	setup $1 $2 $3
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap.sh ../config/$1 ../../data/$1/$2 50GB 20GB"
	rsync -zPrt -e ssh root@$IP:~/data/$1 $output_dir/
	../helper/hotrap-plot.sh $output_dir/$1/$2
	./delete.py $config_file $instance_id
}

for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-accessed
	run_hotrap $workload flush-stably-hot
done
wait
