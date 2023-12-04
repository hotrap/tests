#!/usr/bin/env bash
timestamp_0p=$(hjson-cli -j < info.json | jq -r ".\"run-start-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
awk "
	BEGIN {
		time = 0
	}
	{
		if ($timestamp_0p <= \$1 * 1e9 && \$1 * 1e9 < $timestamp_100p) {
			time += \$2 / 100
		}
	}
	END {
		print time
	}
" < cpu
