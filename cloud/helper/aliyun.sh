sudo sed -i '/^\(root hard nofile 65535\|\* hard nofile 65535\)$/d' /etc/security/limits.conf

sudo mkfs.ext4 /dev/nvme0n1
sudo mkdir /mnt/fd
sudo mount /dev/nvme0n1 /mnt/fd
sudo chown $USER:$USER /mnt/fd
mkdir -p /mnt/fd/{db,fd,viscnts}
sudo bash -c "echo \"/dev/nvme0n1 /mnt/fd ext4 defaults,nofail 0 0\" >> /etc/fstab"

mkdir testdb
cd testdb
ln -s /mnt/fd/{db,fd,viscnts} .
mkdir sd
cd ..

# Sometimes fd_dev would be nvme0c0n1
echo "export fd_dev=$(iostat | grep "nvme0" | awk '{print $1}')" >> ~/.profile
echo 'export sd_dev=vda' >> ~/.profile


mkdir -p ~/.cargo
cat >> ~/.cargo/config <<EOF
[source.crates-io]
replace-with = 'rsproxy'

[source.rsproxy]
registry = "https://rsproxy.cn/crates.io-index"

[registries.rsproxy]
index = "https://rsproxy.cn/crates.io-index"

[net]
git-fetch-with-cli = true
EOF
cat >> ~/.profile <<EOF
export RUSTUP_DIST_SERVER="https://rsproxy.cn"
export RUSTUP_UPDATE_ROOT="https://rsproxy.cn/rustup"
EOF
source ~/.profile
sh <(curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh) -y
source "$HOME/.cargo/env"

