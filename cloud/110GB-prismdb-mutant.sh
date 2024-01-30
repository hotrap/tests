if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

workloads=(
	"workload_110GB_wr_hotspot0.05"
	"workload_110GB_wr_uniform"
	"workload_110GB_wr_zipfian"
	"workload_110GB_wh_hotspot0.05"
	"workload_110GB_wh_uniform"
	"workload_110GB_wh_zipfian"
	"workload_110GB_ycsba_hotspot0.05"
	"workload_110GB_ycsba_uniform"
	"workload_110GB_ycsba_zipfian"
	"workload_110GB_ycsbc_hotspot0.05"
	"workload_110GB_ycsbc_uniform"
	"workload_110GB_ycsbc_zipfian"
)

source common.sh

function run {
	workload=$1
	version=$2
	IP=$3
	if [ -f ../config/${workload}_${version} ]; then
		workload_file=${workload}_${version}
	else
		workload_file=$workload
	fi
	./checkout-$version $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 "source ~/.profile && cd tests/workloads && ./test-$version-110GB.sh ../config/$workload_file ../../data/$workload/$version"
	rsync -zPrt -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/plot-prismdb-mutant.sh $output_dir/$workload/$version
}

for workload in "${workloads[@]}"; do
	cloud-run run $workload prismdb
	cloud-run run $workload mutant
done
wait
