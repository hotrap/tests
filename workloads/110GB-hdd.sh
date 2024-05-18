function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-110GB.sh ../config/$1 $DIR 10GB
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	# Reserve 330MB for VisCnts
	./test-hotrap-110GB.sh ../config/$1 $DIR
	../helper/hotrap-plot.sh $DIR
}
run-rocksdb 'ycsbc_hotspot0.01_load_110GB_run_1GB' rocksdb-fat
run-hotrap 'ycsbc_hotspot0.01_110GB' promote-stably-hot
