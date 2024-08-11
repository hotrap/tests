#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: "$0" workload-file
	exit 1
fi
mydir=$(dirname "$0")
workspace=$(realpath "$mydir"/../..)
workload_file=$(realpath "$1")
value_length=$(grep valuelength "$workload_file" | cut -f2 -d=)
if [ ! "$value_length" ]; then
	value_length=1000
fi
ycsb_gen() {
	(cd $workspace/YCSB &&
		./bin/ycsb $1 basic -P $workload_file -s -p fieldcount=1 -p fieldlength=0 |
			$workspace/tests/helper/bin/trace-cleaner |
			awk "{
				if (\$1 == \"INSERT\" || \$1 == \"UPDATE\" || \$1 == \"RMW\") {
					print \$1, \$3, $value_length
				} else {
					print \$1, \$3
				}
			}"
	)
}
workload=$(basename $workload_file)
prefix=$workspace/YCSB-traces/$workload
if [ ! -f $prefix-load ]; then
	ycsb_gen load > $prefix-load 
fi
if [ ! -f $prefix-run ]; then
	ycsb_gen run > $prefix-run
fi
