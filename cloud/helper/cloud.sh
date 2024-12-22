#!/usr/bin/env sh

sudo apt install -y git
sudo apt install -y patchelf

sudo apt install -y python3-venv
python3 -m venv ~/.venvs/base
echo ". ~/.venvs/base/bin/activate" >> ~/.profile
. ~/.venvs/base/bin/activate

cd $(dirname $0)/../../..
./tests/setup/pip.sh

sudo chown $USER:$USER /mnt/fd
mkdir -p /mnt/fd/db /mnt/fd/fd /mnt/fd/ralt

mkdir -p testdb
cd testdb
ln -s /mnt/fd/db .
ln -s /mnt/fd/fd .
ln -s /mnt/fd/ralt .
mkdir -p sd
cd ..
