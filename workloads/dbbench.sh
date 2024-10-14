function run-rocksdb {
	../helper/checkout-rocksdb-tiered
	DIR=../../data/mixgraph/rocksdb-tiered
	./dbbench-rocksdb-tiered.sh "$DIR"
	../helper/dbbench-rocksdb-plot.sh "$DIR"
}
function run-hotrap {
	../helper/checkout-hotrap
	DIR=../../data/mixgraph/hotrap
	./dbbench-hotrap.sh "$DIR"
	../helper/dbbench-hotrap-plot.sh "$DIR"
}
run-rocksdb
run-hotrap
