#!/usr/bin/env bash
timestamp_0p=$(hjson-cli -j < info.json | jq -r ".\"run-start-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
function throughput {
	awk "
		BEGIN {
			rkB = 0
			wkB = 0
		}
		{
			if (NR > 1 && $timestamp_0p <= \$1 && \$1 < $timestamp_100p) {
				rkB += \$3
				wkB += \$5
			}
		}
		END {
			print \"read\", rkB / 1e6, \"GB\";
			print \"write\", wkB / 1e6, \"GB\";
			print \"total\", (rkB + wkB) / 1e6, \"GB\"
		}
	" < $1
}
echo SD
throughput iostat-sd.txt
echo CD
throughput iostat-cd.txt
