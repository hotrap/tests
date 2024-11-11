function run-hotrap {
	../helper/checkout-$1
	DIR=../../data/mixgraph-1e7/$1
	./dbbench-1e7-hotrap.sh "$DIR"
	../helper/dbbench-1e7-hotrap-plot.sh "$DIR"
}
run-hotrap range-scan-splay
