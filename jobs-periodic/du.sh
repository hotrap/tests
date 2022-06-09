#!/usr/bin/env bash

while true; do
	echo -n "$(date +%s%N) "
	du -sh /tmp/rocksdb/db/ /tmp/rocksdb/sd/ /tmp/rocksdb/cd/ | awk '{print $1}' | xargs echo
	sleep 1
done
