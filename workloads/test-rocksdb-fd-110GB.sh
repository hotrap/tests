#!/usr/bin/env bash
$(dirname $0)/test-rocksdb-fd-110GB-generic.sh $1 $2 "LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4" $3
