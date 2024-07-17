pip3 install pandas matplotlib humanfriendly json5
pip3 install aliyun-python-sdk-ecs

sh <(curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf) -y
source ~/.cargo/env

cargo install huniq

cd helper
make
cd ..
cd simulations
make
cd ..

cd ..
mkdir data

git clone -b v2023.11.20.00-debian12 https://github.com/seekstar/CacheLib.git
cd CacheLib
./contrib/build.sh -j -p $(realpath ..)/opt/cachelib
cd ..
cat >> ~/.profile <<EOF
export CACHELIB_HOME=$(pwd)/opt/cachelib
export CPLUS_INCLUDE_PATH=\$CACHELIB_HOME/include:\$CPLUS_INCLUDE_PATH
export LIBRARY_PATH=\$CACHELIB_HOME/lib:\$LIBRARY_PATH
export LD_LIBRARY_PATH=\$CACHELIB_HOME/lib:\$LD_LIBRARY_PATH
EOF

git clone git@github.com:hotrap/hotrap.git rocksdb
cp -r rocksdb hotrap
git clone git@github.com:hotrap/SAS-Cache.git
git clone --recursive git@github.com:hotrap/prismdb.git
git clone git@github.com:hotrap/mutant.git

git clone --recursive git@github.com:hotrap/kvexe.git
cp -r kvexe kvexe-rocksdb
cd kvexe-rocksdb
rm -r 3rdparty/{rcu-vector,counter-timer-vec}
git checkout rocksdb
cd ..
git clone -b SAS-Cache --recursive git@github.com:hotrap/kvexe.git kvexe-SAS-Cache
git clone -b prismdb --recursive git@github.com:hotrap/kvexe.git kvexe-prismdb
git clone -b mutant --recursive git@github.com:hotrap/kvexe.git kvexe-mutant

git clone --recursive git@github.com:hotrap/RALT.git

echo Need to setup manually:
echo 1. testdb/{db,fd,sd,viscnts}
echo 2. export fd_dev=the device in \"iostat\" that is used as FD.
echo 3. export sd_dev=the device in \"iostat\" that is used as SD.
echo 4. Restart your shell to make changes take effect
