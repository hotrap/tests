set -e
workload_file=../workloads/workload_1e6_4e7_read_0.5_insert_0.5_latest
# SD=4GB
DIR=../../data/latest/rocksdb
./rocksdb.sh 4GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/latest/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 100 &
../plot/throughput.py $DIR 200 &
../plot/hit.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
