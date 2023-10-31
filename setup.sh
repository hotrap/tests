pip3 install pandas matplotlib humanfriendly
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

git clone git@github.com:hotrap/hotrap.git rocksdb
cp -r rocksdb hotrap

git clone --recursive git@github.com:hotrap/kvexe.git
cp -r kvexe kvexe-rocksdb
cd kvexe-rocksdb
rm -r 3rdparty/{rcu-vector,counter-timer-vec}
git checkout rocksdb
cd ..

git clone git@github.com:hotrap/viscnts-splay-rs.git
git clone --recursive git@github.com:hotrap/viscnts-lsm.git

echo Need to setup manually:
echo 1. testdb/{db,sd,cd,viscnts}
echo 2. export sd_dev=the device in \"iostat\" that is used as SD.
echo 3. export cd_dev=the device in \"iostat\" that is used as CD.
echo 4. It is recommended to restart your shell to make changes take effect
