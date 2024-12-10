#!/usr/bin/env sh

$(dirname $0)/../../setup/rustup-cn.sh

sudo sed -i '/^\(root hard nofile 65535\|\* hard nofile 65535\)$/d' /etc/security/limits.conf

sudo mkfs.ext4 /dev/nvme0n1
sudo mkdir /mnt/fd
sudo mount /dev/nvme0n1 /mnt/fd
sudo sh -c "echo \"/dev/nvme0n1 /mnt/fd ext4 defaults,nofail 0 0\" >> /etc/fstab"

# Sometimes fd_dev would be nvme0c0n1
echo "export fd_dev=$(iostat | grep "nvme0" | awk '{print $1}')" >> ~/.profile
echo 'export sd_dev=vda' >> ~/.profile
