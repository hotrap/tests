#!/usr/bin/env sh
timestamp_0p=$(hjson-cli -j < info.json | jq -r ".\"run-start-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
throughput() {
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
			print \"read\", rkB * 1024 / 1e9, \"GB\";
			print \"write\", wkB * 1024 / 1e9, \"GB\";
			print \"total\", (rkB + wkB) * 1024 / 1e9, \"GB\"
		}
	" < $1
}
fd_res=$(throughput iostat-fd.txt)
echo "$fd_res" | awk '{print "FD", $0}'
sd_res=$(throughput iostat-sd.txt)
echo "$sd_res" | awk '{print "SD", $0}'
fd_total=$(echo "$fd_res" | awk '{if (NR == 3) print $2}')
sd_total=$(echo "$sd_res" | awk '{if (NR == 3) print $2}')
echo "total $(echo $fd_total + $sd_total | bc) GB"
