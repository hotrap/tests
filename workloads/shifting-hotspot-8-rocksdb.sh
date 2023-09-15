set -e
workload_file=../config/config_read_0.5_insert_0.5_shifting_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9_2e7_2e7
# SD=4GB
DIR=../../data/$(basename $0 .sh)
./hrtg-rocksdb.sh 4GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 1 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 10 &
wait
