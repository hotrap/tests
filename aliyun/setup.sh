#!/usr/bin/env bash

if [ ! $1 ]; then
	echo Usage: $0 IP
	exit 1
fi
# https://stackoverflow.com/questions/21383806/how-can-i-force-ssh-to-accept-a-new-host-fingerprint-from-the-command-line
ssh-keygen -R $1
# https://unix.stackexchange.com/questions/33271/how-to-avoid-ssh-asking-permission
while ! ssh root@$1 -o StrictHostKeyChecking=no "true"; do
	sleep 1
done
mydir=$(realpath $(dirname $0))
cd $mydir
ssh root@$1 "bash -s" -- < helper/aliyun-1.sh
rsync -zPrL -e ssh .. root@$1:~/tests --exclude='target'
ssh root@$1 "bash -s" -- < helper/aliyun-2.sh
