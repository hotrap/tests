set -e
workload_file=../workloads/workload_2e7_2e7_read_1_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
# SD=4GB
DIR=../../data/hotspot-ro-rocksdb
./rocksdb.sh 4GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait

