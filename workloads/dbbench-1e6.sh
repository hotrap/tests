function run-rocksdb {
	../helper/checkout-rocksdb-tiered
	DIR=../../data/mixgraph-1e6/rocksdb-tiered
	./dbbench-rocksdb-tiered-generic.sh "$DIR" 1000000
	../helper/dbbench-1e6-rocksdb-plot.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph-1e6/$1
	./dbbench-hotrap-generic.sh "$DIR" 1000000
	../helper/dbbench-1e6-hotrap-plot.sh "$DIR"
}
run-rocksdb
run-hotrap range-scan-splay
