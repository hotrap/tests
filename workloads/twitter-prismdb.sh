workloads=(
	"cluster51-175x"
)

function run-prismdb {
	../helper/checkout-prismdb
	DIR=../../data/$1/prismdb
	echo Result directory: $DIR
	./test-prismdb-replay-110GB.sh ../../twitter/processed/$1 $DIR
}

for workload in "${workloads[@]}"; do
	run-prismdb $workload prismdb
done
