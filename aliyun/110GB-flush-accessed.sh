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
	"ycsbc_uniform_110GB"
)

source common.sh

function run_hotrap_1 {
	setup $1 $2 $3
	# Reserve 250MB for VisCnts
	ssh root@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$1 ../../data/$1/$2 9.75GB 1.1GB"
	rsync -zPrt -e ssh root@$IP:~/data/$1 $output_dir/
	../helper/hotrap-plot.sh $output_dir/$1/$2
	./delete.py $config_file $instance_id
}

for workload in "${workloads[@]}"; do
	run_hotrap $workload flush-accessed
done
wait
