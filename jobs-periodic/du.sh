#!/usr/bin/env bash

echo Timestamp\(ns\) DB SD CD
while true; do
	echo -n "$(date +%s%N) "
	du -sb ~/rocksdb/db/ ~/rocksdb/sd/ ~/rocksdb/cd/ | awk '{print $1}' | xargs echo
	sleep 1
done
