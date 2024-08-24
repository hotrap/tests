#!/usr/bin/env sh

sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir /mnt/sd
sudo mount /dev/nvme1n1 /mnt/sd
sudo chown -R $USER:$USER /mnt/sd
sudo sh -c "echo \"/dev/nvme1n1 /mnt/sd ext4 defaults,nofail 0 0\" >> /etc/fstab"

sudo mkfs.ext4 /dev/nvme2n1
sudo mkdir /mnt/fd
sudo mount /dev/nvme2n1 /mnt/fd
sudo sh -c "echo \"/dev/nvme2n1 /mnt/fd ext4 defaults,nofail 0 0\" >> /etc/fstab"

cd ~
mkdir testdb
cd testdb
ln -s /mnt/sd .
cd ..

echo "export fd_dev=nvme2n1" >> ~/.profile
echo 'export sd_dev=nvme1n1' >> ~/.profile
