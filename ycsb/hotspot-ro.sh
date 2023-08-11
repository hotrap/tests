set -e
workload_file=../workloads/workload_2e7_2e7_read_1_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/hotspot-ro/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 100 &
../plot/throughput.py $DIR 200 &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
# SD=4GB
DIR=../../data/hotspot-ro/rocksdb
./rocksdb.sh 4GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
