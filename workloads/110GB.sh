. $(dirname $0)/common/110GB.sh

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
for workload in "${workloads[@]}"; do
	run-rocksdb $workload rocksdb-fd
	run-rocksdb $workload rocksdb-tiered
	run-version $workload cachelib
	run-version $workload prismdb
	run-version $workload SAS-Cache
	run-hotrap $workload hotrap
done

run-workload "u24685531" hotrap
run-hotrap "ycsbc_uniform_110GB_220GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_110GB_220GB" no-hotness-aware-compaction

run-row-cache "ycsbc_zipfian_110GB_220GB"
run-hotrap "ycsbc_zipfian_110GB_220GB" hotrap-row-cache

workloads=(
	"read_0.5_insert_0.5_hotspot0.05_110GB_220GB"
	"read_0.75_insert_0.25_hotspot0.05_110GB_220GB"
	"read_0.85_insert_0.15_hotspot0.05_110GB_220GB"
	"read_0.9_insert_0.1_hotspot0.05_110GB_220GB"
	"ycsbc_hotspot0.05_110GB_220GB"
)
for workload in "${workloads[@]}"; do
	run-hotrap "$workload" no-promote-by-flush
done
