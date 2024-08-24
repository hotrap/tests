#!/usr/bin/env sh

sudo mkfs.ext4 /dev/nvme1n1    
sudo mkdir /mnt/fd    
sudo mount /dev/nvme1n1 /mnt/fd
sudo sh -c "echo \"/dev/nvme1n1 /mnt/fd ext4 defaults,nofail 0 0\" >> /etc/fstab"

echo "export fd_dev=nvme1n1" >> ~/.profile
echo 'export sd_dev=nvme0n1' >> ~/.profile
