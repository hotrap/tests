#!/usr/bin/env sh
if [ ! $1 ]; then
	echo Usage: $0 output-dir
	exit 1
fi
mydir=$(dirname "$0")
mydir=$(realpath "$mydir")
output_dir=$(realpath "$1")
cd "$mydir/../../testdb/db"
mv LOG "$output_dir"/
