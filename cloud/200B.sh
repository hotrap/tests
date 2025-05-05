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
