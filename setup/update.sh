#!/usr/bin/env sh
set -e

cd $(dirname $0)/..
cd ../rocksdb
git checkout rocksdb
git pull origin

cd ../hotrap
echo hotrap main
git checkout main
git pull origin
git submodule update --init
echo hotrap promote-accessed
git checkout promote-accessed
git pull origin
echo hotrap no-hotness-aware-compaction
git checkout no-hotness-aware-compaction
git pull origin
echo hotrap no-promote-by-flush
git checkout no-promote-by-flush
git pull origin

cd ../RALT
echo RALT main
git checkout main
git pull origin

cd ../kvexe
echo kvexe main
git checkout main
git pull origin
git submodule update --init

cd ../SAS-Cache
echo SAS-Cache
git pull origin
cd ..

if [ -d prismdb ]; then
	cd prismdb
	echo prismdb
	git pull origin
	cd ..
fi

cd kvexe-rocksdb
echo kvexe rocksdb
git checkout rocksdb
git pull origin
git submodule update --init
echo kvexe cachelib
git checkout cachelib
git pull origin
echo kvexe SAS-Cache
git checkout SAS-Cache
git pull origin
echo kvexe prismdb
git checkout prismdb
git pull origin


cd ../tests
git pull origin
cd helper
make
