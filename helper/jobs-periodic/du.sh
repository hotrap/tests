#!/usr/bin/env bash

function work {
	cd ../../../testdb/
	echo Timestamp\(ns\) DB SD CD VisCnts
	while true; do
		echo -n "$(date +%s%N) "
		du -sb db/ sd/ cd/ viscnts/ | awk '{print $1}' | xargs echo
		sleep 1
	done
}
if [ $1 ]; then
	work > $1/du.sh.txt
else
	work
fi
