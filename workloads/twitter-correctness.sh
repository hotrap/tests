workloads=(
	"cluster02-283x"
	"cluster05"
	"cluster07-12x"
	"cluster09-113x"
	"cluster10"
	"cluster12"
	"cluster13"
	"cluster14-3x"
	"cluster15"
	"cluster17-80x"
	"cluster18-186x"
	"cluster20-16x"
	"cluster21-3x"
	"cluster22-9x"
	"cluster23"
	"cluster24-11x"
	"cluster25-223x"
	"cluster26-8x"
	"cluster29"
	"cluster31-2x"
	"cluster32"
	"cluster34-9x"
	"cluster40-5x"
	"cluster41-6x"
	"cluster46"
	"cluster50"
	"cluster52-3x"
	"cluster53-12x"
)
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

for workload in "${workloads[@]}"; do
	../helper/unzstd-processed.sh $workload
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
	../helper/delete-uncompressed.sh $workload
done
