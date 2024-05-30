workloads=(
	"read_0.75_insert_0.25_hotspot0.05_11GB"
	"read_0.5_insert_0.5_hotspot0.05_11GB"
	"ycsba_hotspot0.05_11GB"
	"ycsbc_hotspot0.05_11GB"
	"read_0.5_insert_0.5_uniform_11GB"
	"ycsba_uniform_11GB"
	"ycsbc_uniform_11GB"
	"read_0.5_insert_0.5_zipfian_11GB"
	"ycsba_zipfian_11GB"
	"ycsbc_zipfian_11GB"
)
function run-rocksdb-fd {
	../helper/checkout-rocksdb
	DIR=../../data/$1/rocksdb-fd
	echo Result directory: $DIR
	./test-rocksdb-fd-correctness-11GB.sh $1 $DIR
	../helper/rocksdb-plot-11GB.sh $DIR
}
function run-hotrap {
	../helper/checkout-$2
	DIR=../../data/$1/$2
	echo Result directory: $DIR
	./test-hotrap-correctness-11GB.sh $1 $DIR
	../helper/hotrap-plot-11GB.sh $DIR
	diff $DIR/ans.sha256 ../../data/$1/rocksdb-fd/ans.sha256
}
for workload in "${workloads[@]}"; do
	workspace=$(realpath ../..)
	workload_file=$(realpath ../config/$workload)
	function ycsb-gen {
		(cd $workspace/YCSB &&
			./bin/ycsb $1 basic -P $workload_file -s -p fieldcount=1 -p fieldlength=0 |
				$workspace/tests/helper/bin/trace-cleaner |
				awk '{
					if ($1 == "INSERT" || $1 == "UPDATE" || $1 == "RMW") {
						print $1, $3, 1000
					} else {
						print $1, $3
					}
				}'
		)
	}
	if [ ! -f $workspace/YCSB-traces/$workload-load ]; then
		ycsb-gen load > $workspace/YCSB-traces/$workload-load 
	fi
	if [ ! -f $workspace/YCSB-traces/$workload-run ]; then
		ycsb-gen run > $workspace/YCSB-traces/$workload-run
	fi

	run-rocksdb-fd $workload
	run-hotrap $workload promote-stably-hot
	run-hotrap $workload viscnts-splay-rs
done
run-hotrap "ycsbc_uniform_11GB" promote-accessed
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" no-retain
run-hotrap "read_0.75_insert_0.25_hotspot0.05_11GB" no-promote-by-compaction
