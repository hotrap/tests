set -e
cat $1/latency_* | ~/tests/helper/calc-latency > $1/_latency_result
rm $1/latency_*
mv $1/_latency_result $1/latency_result
