set -e
workload_file=../config/ycsbc_zipfian_20GB
DIR=../../data/$(basename $0 .sh)
./ycsb-rocksdb.sh 6GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
wait
