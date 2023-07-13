set -e
workload_file=../workloads/workload_1e6_4e7_read_0.5_insert_0.5_latest
# SD=4GB
DIR=../../data/latest-4/rocksdb
./rocksdb.sh 4GB $workload_file $DIR 4
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/latest-4/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR 4
