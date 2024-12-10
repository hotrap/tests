function run-rocksdb {
	../helper/checkout-rocksdb-tiered
	DIR=../../data/mixgraph/rocksdb-tiered
	./dbbench-rocksdb-tiered.sh "$DIR"
	../helper/dbbench-rocksdb-plot.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph/$1
	./dbbench-hotrap.sh "$DIR"
	../helper/dbbench-hotrap-plot.sh "$DIR"
}
run-rocksdb
run-hotrap hotrap
run-hotrap viscnts-splay-rs
run-hotrap range-scan
run-hotrap range-scan-splay
