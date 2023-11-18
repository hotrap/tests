#!/usr/bin/env bash
timestamp_70p=$(hjson-cli -j < info.json | jq -r ".\"run-70%-timestamp(ns)\"")
timestamp_100p=$(hjson-cli -j < info.json | jq -r ".\"run-end-timestamp(ns)\"")
awk "{
	if (NR > 1 && $timestamp_70p <= \$1 && \$1 < $timestamp_100p)
		print \$0
}" < promoted-or-retained-bytes | awk '
	{
		if (NR == 1) {
			first_by_flush = $2;
			first_2sdlast = $3;
			first_2cdfront = $4;
			first_retained = $5;
		}
	}
	END {
		print "by-flush", $2 - first_by_flush;
		print "2sdlast", $3 - first_2sdlast;
		print "2cdfront", $4 - first_2cdfront;
		print "retained", $5 - first_retained;
	}
'
