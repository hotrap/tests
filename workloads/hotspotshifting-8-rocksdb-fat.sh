set -e
workload_file=../config/ycsbc_hotspotshifting0.1_20GB
DIR=../../data/$(basename $0 .sh)
./ycsb-rocksdb.sh 6GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 1 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 10 &
wait
