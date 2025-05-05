#!/usr/bin/env sh
set -e
total_time=0
while true; do
	if ! read workload; then
		break
	fi
	if [ ! -d $workload ]; then
		continue
	fi
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
			echo "Fail to read load time: $workload/$version"
		fi
		if run_time=$(hjson-cli -j < info.json | jq -er ".\"run-time(secs)\""); then
			total_time=$(echo $total_time + $run_time | bc -l)
		else
			echo "Fail to read run time: $workload/$version"
		fi
		cd ..
	done
	cd ..
done
echo $total_time
