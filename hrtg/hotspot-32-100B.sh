set -e
workload_file=../workloads/config_4e8_read_0.5_insert_0.5_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9_valuelength_100
# SD=4GB
# DIR=../../data/hotspot-32-100B/rocksdb
# ./rocksdb.sh 4GB $workload_file $DIR 32
# mkdir -p $DIR/plot/
# ../plot/ops.py $DIR 50 &
# ../plot/tps.py $DIR 50 &
# ../plot/throughput.py $DIR 100 &
# ../plot/latency.py < $DIR/latency > $DIR/plot/latency &
# wait
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/hotspot-32-100B/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR 32
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 100 &
../plot/throughput.py $DIR 200 &
../plot/hit.py $DIR &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
