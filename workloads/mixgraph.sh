function run-rocksdb {
	../helper/checkout-rocksdb-tiered
	DIR=../../data/mixgraph/rocksdb-tiered
	./mixgraph-rocksdb-tiered-generic.sh "$DIR" 420000000
	../helper/dbbench-rocksdb-plot.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph/$1
	./mixgraph-hotrap-generic.sh "$DIR" 420000000
	../helper/dbbench-hotrap-plot.sh "$DIR"
}
run-rocksdb
run-hotrap hotrap
run-hotrap viscnts-splay-rs
run-hotrap range-scan
run-hotrap range-scan-splay
