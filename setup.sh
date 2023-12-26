pip3 install pandas matplotlib humanfriendly json5
pip3 install aliyun-python-sdk-ecs

tmp=$(mktemp)
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf > $tmp
sh $tmp -y
rm $tmp
source ~/.cargo/env

cd helper
make
cd ..
cd simulations
make
cd ..

cd ..
mkdir data

git clone -b v2023.11.20.00 https://github.com/facebook/CacheLib.git
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

git clone --recursive git@github.com:hotrap/kvexe.git
cp -r kvexe kvexe-rocksdb
cd kvexe-rocksdb
rm -r 3rdparty/{rcu-vector,counter-timer-vec}
git checkout rocksdb
cd ..
git clone -b secondary-cache --recursive git@github.com:hotrap/kvexe.git kvexe-secondary-cache

git clone git@github.com:hotrap/viscnts-splay-rs.git
git clone --recursive git@github.com:hotrap/viscnts-lsm.git

echo Need to setup manually:
echo 1. testdb/{db,sd,cd,viscnts}
echo 2. export sd_dev=the device in \"iostat\" that is used as SD.
echo 3. export cd_dev=the device in \"iostat\" that is used as CD.
echo 4. Restart your shell to make changes take effect
