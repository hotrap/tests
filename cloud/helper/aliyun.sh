sudo sed -i '/^\(root hard nofile 65535\|\* hard nofile 65535\)$/d' /etc/security/limits.conf

sudo mkfs.ext4 /dev/nvme0n1
sudo mkdir /mnt/sd
sudo mount /dev/nvme0n1 /mnt/sd
sudo chown $USER:$USER /mnt/sd
mkdir -p /mnt/sd/{db,sd,viscnts}
sudo bash -c "echo \"/dev/nvme0n1 /mnt/sd ext4 defaults 0 0\" >> /etc/fstab"

mkdir testdb
cd testdb
ln -s /mnt/sd/{db,sd,viscnts} .
mkdir cd
cd ..

# Sometimes sd_dev would be nvme0c0n1
echo "export sd_dev=$(iostat | grep "nvme0" | awk '{print $1}')" >> ~/.profile
echo 'export cd_dev=vda' >> ~/.profile


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

