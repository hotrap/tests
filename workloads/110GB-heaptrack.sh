workload="ycsbc_hotspot0.05_110GB_220GB_200B" 

../helper/checkout-rocksdb
DIR=../../data/$workload/rocksdb-fd-heaptrack
echo Result directory: $DIR
./test-rocksdb-fd-110GB-generic.sh ../config/$workload "$DIR" heaptrack
heaptrack_print "$DIR"/heaptrack.rocksdb-kvexe.*.zst -p -n0 | grep "peak heap memory consumption" | cut -d" " -f5 > "$DIR"/peak-heap-memory-consumption

../helper/checkout-hotrap
DIR=../../data/$workload/hotrap-heaptrack
echo Result directory: $DIR
./test-hotrap-110GB-generic.sh ../config/$workload "$DIR" heaptrack
heaptrack_print "$DIR"/heaptrack.rocksdb-kvexe.*.zst -p -n0 | grep "peak heap memory consumption" | cut -d" " -f5 > "$DIR"/peak-heap-memory-consumption
