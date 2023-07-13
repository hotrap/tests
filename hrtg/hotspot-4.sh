set -e
workload_file=../workloads/config_4e7_read_0.5_insert_0.5_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
# SD=4GB
DIR=../../data/hotspot-4/rocksdb
./rocksdb.sh 4GB $workload_file $DIR 4
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 20 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/hotspot-4/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR 4
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 20 &
#../plot/hit.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
