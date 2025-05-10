function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-$2-110GB.sh ../config/$1 $DIR "$3"
	../helper/rocksdb-plot.sh $DIR
}
function run-version {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-$2-110GB.sh ../config/$1 $DIR "$3"
	../helper/rocksdb-plot.sh $DIR
}
function run-row-cache {
	../helper/checkout-row-cache
	DIR=../../data/$1/row-cache
	echo Result directory: $DIR
	./test-rocksdb-tiered-110GB.sh ../config/$1 $DIR "$2"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR="../../data/$1/$2"
	echo Result directory: $DIR
	./test-hotrap-110GB.sh ../config/$1 $DIR "$3"
	../helper/hotrap-plot.sh $DIR
}
function run-workload {
	workload=$1
	../helper/checkout-$2
	DIR=../../data/$workload/$2
	echo Result directory: $DIR
	./test-hotrap-110GB-generic.sh $DIR "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" "--enable_fast_generator --workload=$workload"
	../helper/hotrap-plot.sh $DIR
}
