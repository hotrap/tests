#!/usr/bin/env bash
timestamp_70p=$(hjson-cli -j < info.json | jq -r ".\"run-70%-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
function throughput {
	awk "
		BEGIN {
			r = 0
			w = 0
		}
		{
			if (NR > 1 && $timestamp_70p <= \$1 && \$1 < $timestamp_100p) {
				r += \$2
				w += \$4
			}
		}
		END {
			seconds = ($timestamp_100p - $timestamp_70p) / 1e9
			print \"read\", r / seconds
			print \"write\", w / seconds
		}
	" < $1
}
echo FD
throughput iostat-fd.txt
echo SD
throughput iostat-sd.txt
