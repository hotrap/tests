#!/usr/bin/env sh
if [ ! "$1" ]; then
	echo Usage: "$0" output-dir
	exit 1
fi
output_dir=$1
if [ ! "$fd_dev" ]; then
	echo Environment variable \"fd_dev\" is not set.
	exit 1
fi
if [ ! "$sd_dev" ]; then
	echo Environment variable \"sd_dev\" is not set.
	exit 1
fi
if [ "$(iostat | grep "$fd_dev")" = "" ]; then
	echo "$fd_dev" does not exist in the output of iostat!
	exit 1
fi
if [ "$(iostat | grep "$sd_dev")" = "" ]; then
	echo "$sd_dev" does not exist in the output of iostat!
	exit 1
fi

echo Timestamp\(ns\) r/s rkB/s w/s wkB/s %util > "$output_dir"/iostat-fd.txt
echo Timestamp\(ns\) r/s rkB/s w/s wkB/s %util > "$output_dir"/iostat-sd.txt

# https://unix.stackexchange.com/questions/29851/shell-script-mktemp-whats-the-best-method-to-create-temporary-named-pipe
tmpdir=$(mktemp -d)
exit_command="rm -r \"$tmpdir\";"
mkfifo "$tmpdir"/pipe
setsid sh -c "
	. $(dirname $0)/../modules/iostat.sh
	process "$fd_dev" < "$tmpdir"/pipe >> "$output_dir"/iostat-fd.txt &
	iostat 1 -x | tee "$tmpdir"/pipe | process "$sd_dev" >> "$output_dir"/iostat-sd.txt
" &
exit_command="${exit_command}kill -TERM -$!;"
# https://newbe.dev/exit-trap-in-dash-vs-ksh-and-bash
trap 'exit 1' INT TERM
trap "$exit_command" EXIT
wait
