set -e
workload_file=../workloads/config_read_0.5_insert_0.5_shifting_hotspot_hotspotdatafraction_0.1_hotspotopnfraction_0.9_2e7_2e7
# SD=4GB
DIR=../../data/shifting-hotspot-4/rocksdb
./rocksdb.sh 4GB $workload_file $DIR 4
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/shifting-hotspot-4/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR 4
