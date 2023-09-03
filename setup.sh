pip3 install pandas matplotlib humanfriendly

tmp=$(mktemp)
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf > $tmp
sh $tmp -y
rm $tmp
source ~/.cargo/env

cd helper
make
cd ..
cd plot/helper
make
cd ../..
cd simulations
make
cd ..

cd ..
mkdir data
git clone https://github.com/brianfrankcooper/YCSB.git

git clone git@github.com:hotrap/hotrap.git rocksdb
cp -r rocksdb hotrap

git clone --recursive git@github.com:hotrap/kvexe.git
cp -r kvexe kvexe-rocksdb
cd kvexe-rocksdb
rm -r 3rdparty/{rcu-vector,counter-timer-vec}
git checkout rocksdb
cd ..

git clone git@github.com:hotrap/viscnts-splay-rs.git

git clone git@github.com:hotrap/trace-generator.git
cd trace-generator
cargo build --release

echo Need to setup manually:
echo 1. testdb/{db,sd,cd,viscnts}
echo 2. Make python points to python2 \(Needed by YCSB\)
echo 3. export sd_dev=the device in \"iostat\" that is used as SD.
echo 4. export cd_dev=the device in \"iostat\" that is used as CD.
echo 5. It is recommended to restart your shell to make changes take effect