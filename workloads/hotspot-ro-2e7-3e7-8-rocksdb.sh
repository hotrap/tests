set -e
workload_file=../config/ycsbc_hotspot0.1_2e7_3e7
DIR=../../data/$(basename $0 .sh)
./ycsb-rocksdb.sh 4GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
wait
