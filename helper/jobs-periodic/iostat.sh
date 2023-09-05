#!/usr/bin/env bash

if [ ! $sd_dev ]; then
	echo Environment variable \"sd_dev\" is not set.
	exit 1
fi
if [ ! $cd_dev ]; then
	echo Environment variable \"cd_dev\" is not set.
	exit 1
fi
if [ "$(iostat | grep $sd_dev)" == "" ]; then
	echo $sd_dev does not exist in the output of iostat!
	exit 1
fi
if [ "$(iostat | grep $cd_dev)" == "" ]; then
	echo /dev/$cd_dev does not exist in the output of iostat!
	exit 1
fi
echo Timestamp\(ns\) sd_tps sd_kB_read/s sd_kB_wrtn/s cd_tps cd_kB_read/s cd_kB_wrtn/s
awk_file=$(mktemp)
# mawk does not respect fflush(stdout)
# Use bash -c to ensure that "date" is executed for every line
iostat 1 | gawk "
{
        if (\"$sd_dev\" == \$1)
                printf \"%s %s %s \",\$2,\$3,\$4
        if (\"$cd_dev\" == \$1) {
                print \$2,\$3,\$4
                fflush(stdout)
        }
}
" | xargs -I {} bash -c 'echo $(date +%s%N) {}'
