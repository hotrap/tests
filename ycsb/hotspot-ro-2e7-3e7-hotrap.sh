set -e
workload_file=../workloads/workload_2e7_3e7_read_1_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/hotspot-ro-2e7-3e7-hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 100 &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
