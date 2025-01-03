#!/usr/bin/env sh

sudo apt install -y fonts-linuxlibertine
# https://stackoverflow.com/a/49884009/13688160
rm ~/.cache/matplotlib -rf

sudo apt install -y g++ cmake libtcmalloc-minimal4 nocache
# tests
sudo apt install -y jq rsync bc hjson-go
# iostat
sudo apt install -y sysstat
# RocksDB
sudo apt install -y libgflags-dev
# RALT
sudo apt install -y libfmt-dev
# kvexe
sudo apt install -y liburcu-dev libboost-program-options-dev libxxhash-dev
# iostat.sh
sudo apt install -y gawk
# CacheLib
sudo apt install -y libjemalloc-dev libevent-dev libdouble-conversion-dev libnuma-dev libboost-regex-dev libsodium-dev libboost-context-dev libboost-filesystem-dev libsnappy-dev libunwind-dev zlib1g-dev libboost-iostreams-dev libdwarf-dev libiberty-dev liburing-dev
# SAS-Cache
sudo apt install -y libssl-dev libbz2-dev liblz4-dev libaio-dev
# PrismDB
sudo apt install -y libtbb-dev
# twitter trace
sudo apt install -y time

# Correctness checking
sudo apt install -y maven
