workloads=(
	"cluster02-283x"
	"cluster05"
	"cluster07-12x"
	"cluster09-113x"
	"cluster10"
	"cluster11-25x"
	"cluster12"
	"cluster13"
	"cluster14-3x"
	"cluster15"
	"cluster16-67x"
	"cluster17-80x"
	"cluster18-186x"
	"cluster19-3x"
	"cluster20-16x"
	"cluster21-3x"
	"cluster22-9x"
	"cluster23"
	"cluster24-11x"
	"cluster25-223x"
	"cluster26-8x"
	"cluster28-18x"
	"cluster29"
	"cluster31-2x"
	"cluster32"
	"cluster34-9x"
	"cluster35"
	"cluster36-18x"
	"cluster38"
	"cluster39"
	"cluster40-5x"
	"cluster41-6x"
	"cluster44-40x"
	"cluster46"
	"cluster48-5x"
	"cluster50"
	"cluster52-3x"
	"cluster53-12x"
)
function run-rocksdb {
	../helper/checkout-rocksdb
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-$2-110GB-replay.sh $prefix $DIR "--enable_fast_process"
	../helper/rocksdb-plot.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-hotrap-110GB-replay.sh $prefix $DIR "--enable_fast_process"
	../helper/hotrap-plot.sh $DIR
}
function run-version {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	prefix=../../twitter/processed/$1
	./test-$2-110GB-replay.sh $prefix $DIR "--enable_fast_process"
	../helper/rocksdb-plot.sh $DIR
}

for workload in "${workloads[@]}"; do
	../helper/unzstd-processed.sh $workload
	run-rocksdb $workload rocksdb-fd
	run-hotrap $workload hotrap
	run-rocksdb $workload rocksdb-tiered
	run-version $workload SAS-Cache
	run-version $workload mutant
	run-version $workload prismdb
	../helper/delete-uncompressed.sh $workload
done
