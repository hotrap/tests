set -e
workload_file=../config/workload_2e7_3e7_read_1_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
SD=4GB
DIR=../../data/$(basename $0 .sh)
./ycsb-rocksdb.sh 4GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/ops.py $DIR 50 &
../plot/tps.py $DIR 50 &
../plot/throughput.py $DIR 100 &
wait
