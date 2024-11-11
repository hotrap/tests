function run-rocksdb {
	../helper/checkout-rocksdb-tiered
	DIR=../../data/mixgraph-unlimited/rocksdb-tiered
	./dbbench-unlimited-rocksdb-tiered.sh "$DIR"
	../helper/dbbench-rocksdb-plot.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph-unlimited/$1
	./dbbench-unlimited-hotrap-generic.sh "$DIR" 420000000
	../helper/dbbench-hotrap-plot.sh "$DIR"
}
run-rocksdb
run-hotrap hotrap
run-hotrap range-scan-splay
