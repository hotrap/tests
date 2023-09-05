set -e
workload_file=../config/config_4e7_read_0.5_insert_0.5_uniform
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/$(basename $0 .sh)
./hrtg-hotrap.sh 4GB 2GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
../plot/hit.py $DIR &
wait
