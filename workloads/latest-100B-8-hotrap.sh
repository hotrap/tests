set -e
workload_file=../workloads/latest_1e6_4e8_read_0.5_insert_0.5_fieldcount_1
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/$(basename $0 .sh)
./ycsb-hotrap.sh 4GB 2GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 10 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
wait
