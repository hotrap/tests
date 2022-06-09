#!/usr/bin/env bash

# timestamp(ns) tps kB_read/s kB_wrtn/s
while true; do
	iostat 1 | awk '{if ("nvme0n1" == $1) printf "%s %s %s ",$2,$3,$4; if ("sda" == $1) print $2,$3,$4}'
done
