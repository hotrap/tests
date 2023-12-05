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
sd_res=$(throughput iostat-sd.txt)
echo "$sd_res" | awk '{print "SD", $0}'
cd_res=$(throughput iostat-cd.txt)
echo "$cd_res" | awk '{print "CD", $0}'
sd_total=$(echo "$sd_res" | awk '{if (NR == 3) print $2}')
cd_total=$(echo "$cd_res" | awk '{if (NR == 3) print $2}')
echo "total $(echo $sd_total + $cd_total | bc) GB"
