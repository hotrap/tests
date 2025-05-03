function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-$2-110GB-replay.sh $prefix $DIR "--export_ans_xxh64"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2-correctness
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-hotrap-110GB-replay.sh $prefix $DIR "--export_ans_xxh64"
	../helper/hotrap-plot.sh $DIR
	../tools/check-ans.sh ../../data/$1/rocksdb-fd-correctness/ $DIR/
}

workloads=(
	"cluster02-283x"
	"cluster11-25x"
	"cluster15"
	"cluster16-67x"
	"cluster17-80x"
	"cluster18-186x"
	"cluster19-3x"
	"cluster22-9x"
	"cluster23"
	"cluster29"
	"cluster46"
	"cluster48-5x"
	"cluster51-175x"
	"cluster53-12x"
)
for workload in "${workloads[@]}"; do
	../helper/unzstd-processed.sh $workload
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
	../helper/delete-uncompressed.sh $workload
done
