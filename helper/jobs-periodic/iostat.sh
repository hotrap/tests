#!/usr/bin/env bash

if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
if [ ! $fd_dev ]; then
	echo Environment variable \"fd_dev\" is not set.
	exit 1
fi
if [ ! $sd_dev ]; then
	echo Environment variable \"sd_dev\" is not set.
	exit 1
fi
if [ "$(iostat | grep $fd_dev)" == "" ]; then
	echo $fd_dev does not exist in the output of iostat!
	exit 1
fi
if [ "$(iostat | grep $sd_dev)" == "" ]; then
	echo /dev/$sd_dev does not exist in the output of iostat!
	exit 1
fi

function process {
	# mawk does not respect fflush(stdout)
	# Use bash -c to ensure that "date" is executed for every line
	gawk "
	{
			if (\"$1\" == \$1) {
					print \$2,\$3,\$8,\$9,\$23
					fflush(stdout)
			}
	}
	" | xargs -I {} bash -c 'echo $(date +%s%N) {}'
}

echo Timestamp\(ns\) r/s rkB/s w/s wkB/s %util > $1/iostat-fd.txt
echo Timestamp\(ns\) r/s rkB/s w/s wkB/s %util > $1/iostat-sd.txt
iostat 1 -x | tee >(process $fd_dev >> $1/iostat-fd.txt) | process $sd_dev >> $1/iostat-sd.txt
