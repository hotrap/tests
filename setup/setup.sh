#!/usr/bin/env sh
cd "$(dirname $0)"

cd ../helper
make
cd ..
cd simulations
make
cd ..

cd ..
mkdir data

cat >> ~/.profile <<EOF
export CACHELIB_HOME=$(pwd)/opt/cachelib
export CPLUS_INCLUDE_PATH=\$CACHELIB_HOME/include:\$CPLUS_INCLUDE_PATH
export LIBRARY_PATH=\$CACHELIB_HOME/lib:\$LIBRARY_PATH
export LD_LIBRARY_PATH=\$CACHELIB_HOME/lib:\$LD_LIBRARY_PATH
export CMAKE_PREFIX_PATH=\$CACHELIB_HOME/lib/cmake:\$CMAKE_PREFIX_PATH
EOF
. ~/.profile
git clone -b v2023.11.20.00-debian12 https://github.com/hotrap/CacheLib.git
cd CacheLib
./contrib/build.sh -j -p $(realpath ..)/opt/cachelib
cd ..

git clone --recursive https://github.com/hotrap/hotrap.git hotrap
git clone -b rocksdb https://github.com/hotrap/hotrap.git rocksdb
git clone https://github.com/hotrap/SAS-Cache.git
git clone --recursive https://github.com/hotrap/prismdb.git

git clone --recursive https://github.com/hotrap/kvexe.git
git clone -b rocksdb --recursive https://github.com/hotrap/kvexe.git kvexe-rocksdb

git clone --recursive https://github.com/hotrap/RALT.git

# Correctness checking
git clone https://github.com/brianfrankcooper/YCSB.git

echo Need to setup manually:
echo 1. testdb/{db,fd,sd,ralt}
echo 2. export fd_dev=the device in \"iostat\" that is used as FD.
echo 3. export sd_dev=the device in \"iostat\" that is used as SD.
echo 4. Restart your shell to make changes take effect
