. $(dirname $0)/common/110GB.sh

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

for workload in "${hotspot_workloads[@]}"; do
	run-hotrap $workload hotrap
	run-rocksdb $workload rocksdb-fd
done
for workload in "${uniform_workloads[@]}"; do
	run-hotrap $workload hotrap
	run-rocksdb $workload rocksdb-tiered
done
