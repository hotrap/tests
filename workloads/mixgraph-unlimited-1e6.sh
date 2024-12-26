function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/mixgraph-unlimited-1e6/rocksdb-tiered
	./mixgraph-unlimited-rocksdb-tiered-generic.sh "$DIR" 1000000
	../helper/dbbench-rocksdb-plot.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph-unlimited-1e6/$1
	./mixgraph-unlimited-hotrap-generic.sh "$DIR" 1000000
	../helper/dbbench-hotrap-plot.sh "$DIR"
}
run-rocksdb
run-hotrap hotrap
run-hotrap range-scan-splay
