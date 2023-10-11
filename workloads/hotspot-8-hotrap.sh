set -e
workload_file=../config/workload_2e7_2e7_read_0.5_insert_0.5_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9
DIR=../../data/$(basename $0 .sh)
./ycsb-hotrap.sh 6GB 2GB $workload_file $DIR 8
mkdir -p $DIR/plot/
../plot/du.py $DIR &
../plot/ops.py $DIR 1 &
../plot/tps.py $DIR 1 &
../plot/throughput.py $DIR 10 &
../plot/hit.py $DIR &
../plot/promoted-bytes.py $DIR &
wait
