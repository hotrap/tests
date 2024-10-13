../helper/checkout-hotrap
DIR=../../data/mixgraph/hotrap
./dbbench-hotrap.sh "$DIR"
../helper/dbbench-hotrap-plot.sh "$DIR"
