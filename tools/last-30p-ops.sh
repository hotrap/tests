#!/usr/bin/env bash
timestamp_70p=$(hjson-cli -j < info.json | jq -r ".\"run-70%-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
awk "{
	if (NR > 1 && $timestamp_70p <= \$1 && \$1 < $timestamp_100p)
		print \$0
}" < progress | awk '{
	if (NR == 1) {
		first_timestamp = $1;
		first_progress = $2;
	}
}
END {
	print ($2 - first_progress) / (($1 - first_timestamp) / 1e9)
}'
