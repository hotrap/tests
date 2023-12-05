#!/usr/bin/env bash
timestamp_0p=$(hjson-cli -j < info.json | jq -r ".\"run-start-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
awk "{
	if (NR > 1 && $timestamp_0p <= \$1 && \$1 < $timestamp_100p)
		print \$0
}" < cputimes | awk '{
	if (NR == 1) {
		first_cputimes = $2;
	}
}
END {
	print $2 - first_cputimes
}'
