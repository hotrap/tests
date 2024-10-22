#!/usr/bin/env sh

work() {
	cd ../../../testdb/
	echo Timestamp\(ns\) DB FD SD RALT
	while true; do
		echo -n "$(date +%s%N) "
		du -sb db/ fd/ sd/ ralt/ | awk '{print $1}' | xargs echo
		sleep 1
	done
}
if [ $1 ]; then
	work > $1/du.sh.txt
else
	work
fi
