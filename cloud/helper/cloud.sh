sudo apt install -y git
sudo apt install -y patchelf

sudo apt install -y python3-venv
python3 -m venv ~/.venvs/base
echo ". ~/.venvs/base/bin/activate" >> ~/.profile
. ~/.venvs/base/bin/activate

pip3 install humanfriendly
