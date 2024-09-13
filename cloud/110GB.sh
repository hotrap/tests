if [[ $# != 2 ]]; then
	echo Usage: $0 config-file output-dir
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

. ./common.sh

function run-rocksdb-fd {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-rocksdb-fd-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-$version $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-$version-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-hotrap {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-hotrap-110GB.sh ../config/$workload ../../data/$workload/$version \"${@:4}\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}
function run-u135542 {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-hotrap-110GB-generic.sh ../../data/$workload/$version \"LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4\" \"--enable_fast_generator --workload=$workload --switches=0x1 ${@:4}\""
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/hotrap-plot.sh $output_dir/$workload/$version
}

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)
check-workload-files "${workloads[@]}"

for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb-fd $workload rocksdb-fd
	cloud-run run-rocksdb $workload rocksdb-tiered
	cloud-run run-rocksdb $workload mutant
	cloud-run run-rocksdb $workload prismdb
	cloud-run run-rocksdb $workload SAS-Cache
	cloud-run run-hotrap $workload promote-stably-hot
done
cloud-run run-u135542 "u135542" promote-stably-hot
cloud-run run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
cloud-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-retain
cloud-run run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-compaction

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb $workload kvexe-cachelib
done

workloads=(
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	cloud-run run-rocksdb $workload kvexe-cachelib
done

hotspot_workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB_200B"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB_200B"
	"ycsba_hotspot0.05_110GB_220GB_200B"
	"ycsbc_hotspot0.05_110GB_220GB_200B"
)
uniform_workloads=(
	"read_0.5_insert_0.5_uniform_110GB_220GB_200B"
	"read_0.75_insert_0.25_uniform_110GB_220GB_200B"
	"ycsba_uniform_110GB_220GB_200B"
	"ycsbc_uniform_110GB_220GB_200B"
)
check-workload-files "${hotspot_workloads[@]}"
check-workload-files "${uniform_workloads[@]}"

for workload in "${hotspot_workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot
	cloud-run run-rocksdb-fd $workload rocksdb-fd
done
for workload in "${uniform_workloads[@]}"; do
	cloud-run run-hotrap $workload promote-stably-hot
	cloud-run run-rocksdb $workload rocksdb-tiered
done
wait
