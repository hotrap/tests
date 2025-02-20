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

function run-rocksdb {
	workload=$1
	version=$2
	IP=$3
	./checkout-rocksdb $user $IP
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-$version-110GB.sh ../config/$workload ../../data/$workload/$version"
	rsync -zrpt --partial -e ssh $user@$IP:~/data/$workload $output_dir/
	../helper/rocksdb-plot.sh $output_dir/$workload/$version
}
function run-version {
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
function run-workload {
	workload=$1
	version=$2
	IP=$3
	./checkout-hotrap $user $IP $version
	ssh $user@$IP -o ServerAliveInterval=60 ". ~/.profile && cd tests/workloads && ./test-hotrap-110GB-generic.sh ../../data/$workload/$version \"LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4\" \"--enable_fast_generator --workload=$workload ${@:4}\""
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
	cloud-run machine-config/110GB.json run-rocksdb $workload rocksdb-fd
	cloud-run machine-config/110GB.json run-rocksdb $workload rocksdb-tiered
	cloud-run machine-config/110GB.json run-version $workload prismdb
	cloud-run machine-config/110GB.json run-version $workload SAS-Cache
	cloud-run machine-config/110GB.json run-version $workload cachelib
	cloud-run machine-config/110GB.json run-hotrap $workload hotrap
done
cloud-run machine-config/110GB.json run-workload "u24685531" hotrap
cloud-run machine-config/110GB.json run-workload "2-4-6-8" hotrap
cloud-run machine-config/110GB.json run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
cloud-run machine-config/110GB.json run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-retain
cloud-run machine-config/110GB.json run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-compaction
cloud-run machine-config/110GB.json run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-hotness-aware-compaction

cloud-run machine-config/110GB.json run-hotrap "read_0.5_insert_0.5_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "read_0.85_insert_0.15_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "read_0.95_insert_0.05_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "ycsbc_hotspot0.05_110GB_220GB" no-promote-by-flush

workloads=(
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"ycsba_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_zipfian_110GB_220GB"
	"ycsba_zipfian_110GB_220GB"
	"ycsbc_zipfian_110GB_220GB"
	"read_0.75_insert_0.25_uniform_110GB_220GB"
	"ycsbc_uniform_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	cloud-run machine-config/110GB.json run-version $workload mutant
done

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.5_insert_0.5_zipfian_110GB_220GB"
	"read_0.5_insert_0.5_uniform_110GB_220GB"
	"ycsba_uniform_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	cloud-run machine-config/110GB.json run-version $workload mutant "--run_90p_ops=10000"
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
	cloud-run machine-config/110GB.json run-hotrap $workload hotrap
	cloud-run machine-config/110GB.json run-rocksdb $workload rocksdb-fd
done
for workload in "${uniform_workloads[@]}"; do
	cloud-run machine-config/110GB.json run-hotrap $workload hotrap
	cloud-run machine-config/110GB.json run-rocksdb $workload rocksdb-tiered
done
wait
