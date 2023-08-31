set -e
workload_file=../workloads/workload_2e7_2e7_read_1_uniform
# SD=4GB
DIR=../../data/$(basename $0 .sh)
./rocksdb.sh 4GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 10 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait

