function run-rocksdb {
	../helper/checkout-rocksdb-tiered
	DIR=../../data/mixgraph-1e6/rocksdb-tiered
	./mixgraph-rocksdb-tiered-generic.sh "$DIR" 1000000
	../helper/dbbench-rocksdb-plot-no-smooth.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph-1e6/$1
	./mixgraph-hotrap-generic.sh "$DIR" 1000000
	../helper/dbbench-hotrap-plot-no-smooth.sh "$DIR"
}
run-rocksdb
run-hotrap hotrap
run-hotrap range-scan-splay
