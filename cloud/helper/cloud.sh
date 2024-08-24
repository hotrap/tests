#!/usr/bin/env sh

sudo apt install -y git
sudo apt install -y patchelf

sudo apt install -y python3-venv
python3 -m venv ~/.venvs/base
echo ". ~/.venvs/base/bin/activate" >> ~/.profile
. ~/.venvs/base/bin/activate

./tests/pip.sh

sudo chown $USER:$USER /mnt/fd
mkdir -p /mnt/fd/db /mnt/fd/fd /mnt/fd/viscnts

mkdir -p testdb
cd testdb
ln -s /mnt/fd/db .
ln -s /mnt/fd/fd .
ln -s /mnt/fd/viscnts .
mkdir -p sd
cd ..

tmp=$(mktemp)
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf > $tmp
sh $tmp -y
rm $tmp
. ~/.cargo/env
