#!/usr/bin/env sh
timestamp_70p=$(hjson-cli -j < info.json | jq -r ".\"run-70%-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
awk "{
	if (NR > 1 && $timestamp_70p <= \$1 && \$1 < $timestamp_100p)
		print \$0
}" < promoted-or-retained-bytes | awk '
	{
		if (NR == 1) {
			first_by_flush = $2;
			first_2fdlast = $3;
			first_2sdfront = $4;
			first_retained = $5;
		}
	}
	END {
		print "by-flush", ($2 - first_by_flush) / 1e9, "GB";
		print "2fdlast", ($3 - first_2fdlast) / 1e9, "GB";
		print "2sdfront", ($4 - first_2sdfront) / 1e9, "GB";
		print "retained", ($5 - first_retained) / 1e9, "GB";
	}
'
