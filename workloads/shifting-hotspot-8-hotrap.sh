set -e
workload_file=../config/config_read_0.5_insert_0.5_shifting_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9_2e7_2e7
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/$(basename $0 .sh)
./hrtg-hotrap.sh 4GB 2GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 100 &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
