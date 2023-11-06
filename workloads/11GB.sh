workloads=(
	"ycsba_hotspot0.01_11GB"
	"ycsba_uniform_11GB"
	"ycsba_zipfian_11GB"
	"ycsbb_hotspot0.01_11GB"
	"ycsbb_uniform_11GB"
	"ycsbb_zipfian_11GB"
	"ycsbc_hotspot0.01_11GB"
	"ycsbc_hotspotshifting0.01_11GB"
	"ycsbc_uniform_11GB"
	"ycsbc_zipfian_11GB"
	"ycsbd_hotspot0.01_11GB"
	"ycsbd_uniform_11GB"
	"ycsbd_zipfian_11GB"
	"ycsbf_hotspot0.01_11GB"
	"ycsbf_uniform_11GB"
	"ycsbf_zipfian_11GB"
	"hotspot0.01_11GB_read_0.5_insert_0.5"
	"latest_11GB_read_0.5_insert_0.5"
	"uniform_11GB_read_0.5_insert_0.5"
	"zipfian_11GB_read_0.5_insert_0.5"
	"ycsbc_hotspot0.01_11GB_200B"
	"hotspot0.01_11GB_200B_read_0.5_insert_0.5"
)
function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-11GB.sh ../config/$1 $DIR 1GB
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-11GB.sh ../config/$1 $DIR 1GB 110MB
	../helper/hotrap-plot-11GB.sh $DIR
}
for workload in "${workloads[@]}"; do
	run_hotrap $workload viscnts-splay-rs
	run_hotrap $workload flush-stably-hot
	run_rocksdb $workload rocksdb-fat
done
