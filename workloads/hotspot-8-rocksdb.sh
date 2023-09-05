set -e
workload_file=../config/config_4e7_read_0.5_insert_0.5_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
# SD=4GB
DIR=../../data/$(basename $0 .sh)
./hrtg-rocksdb.sh 4GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/ops.py $DIR 10 &
../plot/tps.py $DIR 10 &
../plot/throughput.py $DIR 100 &
wait
