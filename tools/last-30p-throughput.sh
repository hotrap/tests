#!/usr/bin/env bash
timestamp_70p=$(hjson-cli -j < info.json | jq -r ".\"run-70%-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
function throughput {
	awk "
		BEGIN {
			rkB = 0
			wkB = 0
			cnt = 0
		}
		{
			if (NR > 1 && $timestamp_70p <= \$1 && \$1 < $timestamp_100p) {
				rkB += \$3
				wkB += \$5
				cnt += 1
			}
		}
		END {
			print \"read\", rkB / cnt / 1e6, \"GB/s\"
			print \"write\", wkB / cnt / 1e6, \"GB/s\"
		}
	" < $1
}
echo SD
throughput iostat-sd.txt
echo CD
throughput iostat-cd.txt
