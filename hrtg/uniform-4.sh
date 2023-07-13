set -e
workload_file=../workloads/config_4e7_read_0.5_insert_0.5_uniform
# SD=4GB
DIR=../../data/uniform-4/rocksdb
./rocksdb.sh 4GB $workload_file $DIR 4
# hit_count, delta=2GB, SD=4GB, kAccurateHotSizePromotionSize
DIR=../../data/uniform-4/hotrap
./hotrap.sh 4GB 2GB $workload_file $DIR 4
