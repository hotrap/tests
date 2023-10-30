function run_rocksdb {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-rocksdb.sh ../config/$1 $DIR 32GB
	../helper/rocksdb-plot.sh $DIR
}

function workload {
	cat <<EOF
recordcount=288000000
operationcount=288000000
workload=site.ycsb.workloads.CoreWorkload

readallfields=true

readproportion=0.5
updateproportion=0
scanproportion=0
insertproportion=0.5

requestdistribution=hotspot

hotspotdatafraction=$1
hotspotopnfraction=0$(echo 1 - $1 | bc)
EOF
}
function run_hotrap {
	../helper/checkout-$2
	DIR=../../data/hotspot$1_288GB_read_0.5_insert_0.5/$2
	echo Result directory: $DIR
	./test-hotrap.sh <(workload $1) $DIR 32GB $(echo "$1 * 288" | bc)GB
	../helper/hotrap-plot.sh $DIR
}
hotspots=(0.02 0.03 0.04 0.05)
for hotspot in "${hotspots[@]}"; do
	run_hotrap $hotspot flush-stably-hot
done
