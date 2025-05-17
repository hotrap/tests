#!/usr/bin/env sh
set -e

test_time() (
	workload=$1
	total_time=0
	if [ -d $workload ]; then
		cd $workload
		for version in $(ls); do
			if [ ! -d $version ]; then
				continue
			fi
			if [ ! -f $version/info.json ]; then
				continue
			fi
			cd $version
			if load_time=$(hjson-cli -j < info.json | jq -er ".\"load-time(secs)\""); then
				total_time=$(echo $total_time + $load_time | bc -l)
			else
				echo "Fail to read load time: $workload/$version" 1>&2
			fi
			if run_time=$(hjson-cli -j < info.json | jq -er ".\"run-time(secs)\""); then
				total_time=$(echo $total_time + $run_time | bc -l)
			else
				echo "Fail to read run time: $workload/$version" 1>&2
			fi
			cd ..
		done
		cd ..
	fi
	echo "$total_time"
)

total_time=0
if [ "$1" = "--stdin" ]; then
	while true; do
		if ! read workload; then
			break
		fi
		total_time="$(echo $total_time + $(test_time $workload) | bc -l)"
	done
else
	for workload in $(ls); do
		total_time="$(echo $total_time + $(test_time $workload) | bc -l)"
	done
fi

echo $total_time
