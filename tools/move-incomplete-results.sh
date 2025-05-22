#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: "$0" target-dir
	exit 1
fi
mydir=$(realpath $(dirname $0))
target_dir=$(realpath "$1")
for workload in $(ls); do
	if [ "$(realpath "$workload")" = "$target_dir" ]; then
		continue
	fi
	if [ ! -d "$workload" ]; then
		continue
	fi
	cd "$workload"
	for version in $(ls); do
		if [ ! -d "$version" ]; then
			continue
		fi
		if ! "$mydir"/last-10p-ops "$version" > /dev/null 2>&1; then
			if [ ! -d "$target_dir/$workload" ]; then
				mkdir -p "$target_dir/$workload"
			fi
			command="mv $version $target_dir/$workload/"
			echo "$command"
			$command
		fi
	done
	cd ..
	rm -d "$workload" 2> /dev/null
done
