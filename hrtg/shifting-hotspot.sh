set -e
workload_file=../workloads/config_read_0.5_insert_0.5_shifting_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9_2e7_2e7
# cache_size=0, SD=4GB
DIR=../../data/shifting-hotspot/rocksdb
./rocksdb.sh 4GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 1 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 1 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
# hit_count, cache_size=0, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/shifting-hotspot/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 100 &
../plot/throughput.py $DIR 100 &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
