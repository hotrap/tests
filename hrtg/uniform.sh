set -e
workload_file=../workloads/config_4e7_read_0.5_insert_0.5_uniform
# SD=4GB
DIR=../../data/uniform/rocksdb
./rocksdb.sh 4GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/uniform/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
../plot/hit.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
