set -e
workload_file=../config/workload_1e6_4e7_read_0.5_insert_0.5_zipfian
# SD=4GB
DIR=../../data/$(basename $0 .sh)
./ycsb-rocksdb.sh 4GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 10 &
wait

