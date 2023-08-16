set -e
workload_file=../workloads/workload_2e7_2e7_read_1_uniform
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/uniform-ro-hotrap
./hotrap.sh 4GB 1GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 100 &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
