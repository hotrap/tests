function run-rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb-110GB.sh ../config/$1 $DIR
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR
	../helper/hotrap-plot.sh $DIR
}
run-rocksdb 'ycsbc_hotspot0.01_110GB_1GB' rocksdb-fat
run-hotrap 'ycsbc_hotspot0.01_110GB_220GB' promote-stably-hot
