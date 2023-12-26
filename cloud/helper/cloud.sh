sudo apt install -y git
# cloud/checkout-secondary-cache
sudo apt install -y patchelf

sudo apt install -y python3-venv
python3 -m venv ~/.venvs/base
echo "source ~/.venvs/base/bin/activate" >> ~/.profile
source ~/.venvs/base/bin/activate

pip3 install humanfriendly
