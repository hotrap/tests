#!/usr/bin/env sh
mydir=$(realpath $(dirname $0))
for workload in $(ls); do
	if [ ! -d "$workload" ]; then
		continue
	fi
	cd "$workload"
	for version in $(ls); do
		if [ ! -d "$version" ]; then
			continue
		fi
		cd "$version"
		if ! "$mydir"/last-10p-ops > /dev/null 2>&1; then
			pwd
		fi
		cd ..
	done
	cd ..
done
