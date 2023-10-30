workloads=(
	"latest_144GB_read_0.5_insert_0.5"
	"hotspot0.01_144GB_read_0.5_insert_0.5"
	"uniform_144GB_read_0.5_insert_0.5"
	"zipfian_144GB_read_0.5_insert_0.5"
	"ycsbc_hotspot0.01_144GB"
	"ycsbc_hotspotshifting0.01_144GB"
	"ycsbc_uniform_144GB"
	"ycsbc_zipfian_144GB"
	"ycsba_hotspot0.01_144GB"
	"ycsba_hotspotshifting0.01_144GB"
	"ycsba_uniform_144GB"
	"ycsba_zipfian_144GB"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-144GB.sh ../config/$1 $DIR 16GB
	../helper/rocksdb-plot.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-144GB.sh ../config/$1 $DIR 16GB 1.44GB
	../helper/hotrap-plot.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_rocksdb $workload rocksdb
	run_rocksdb $workload rocksdb-fat
	run_hotrap $workload flush-accessed
	run_hotrap $workload flush-stably-hot
done
