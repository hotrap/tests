#!/usr/bin/env bash

cd ../../../testdb/
echo Timestamp\(ns\) DB SD CD
while true; do
	echo -n "$(date +%s%N) "
	du -sb db/ sd/ cd/ | awk '{print $1}' | xargs echo
	sleep 1
done
