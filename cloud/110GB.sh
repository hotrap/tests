if [[ $# != 3 ]]; then
	echo Usage: $0 config-file output-dir max-running-instances
	exit 1
fi
config_file=$(realpath $1)
output_dir=$(realpath $2)
max_running_instances=$3
user=$(cat $config_file | jq -er ".user")
cd $(dirname $0)

. common/110GB.sh

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
cloud-run machine-config/110GB.json run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
cloud-run machine-config/110GB.json run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-hotness-aware-compaction

cloud-run machine-config/110GB.json run-hotrap "read_0.5_insert_0.5_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "read_0.85_insert_0.15_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "read_0.95_insert_0.05_hotspot0.05_110GB_220GB" no-promote-by-flush
cloud-run machine-config/110GB.json run-hotrap "ycsbc_hotspot0.05_110GB_220GB" no-promote-by-flush
