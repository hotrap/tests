set -e
workload_file=../workloads/config_read_0.5_insert_0.5_shifting_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9_2e7_2e7
# SD=4GB
DIR=../../data/shifting-hotspot-rocksdb
./rocksdb.sh 4GB $workload_file $DIR
mkdir -p $DIR/plot/
../plot/ops.py $DIR 1 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 1 &
../plot/latency.py < $DIR/latency > $DIR/plot/latency &
wait
