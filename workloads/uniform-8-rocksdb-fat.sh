set -e
workload_file=../config/uniform_2e7_2e7_read_0.5_insert_0.5
DIR=../../data/$(basename $0 .sh)
./ycsb-rocksdb.sh 6GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 1 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 10 &
wait
