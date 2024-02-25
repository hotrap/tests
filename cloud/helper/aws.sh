sudo mkfs.ext4 /dev/nvme1n1    
sudo mkdir /mnt/fd    
sudo mount /dev/nvme1n1 /mnt/fd
sudo chown $USER:$USER /mnt/fd
mkdir -p /mnt/fd/{db,fd,viscnts}     
sudo bash -c "echo \"/dev/nvme1n1 /mnt/fd ext4 defaults 0 0\" >> /etc/fstab"

cd ~
mkdir testdb
cd testdb
ln -s /mnt/fd/{db,fd,viscnts} .
mkdir sd
cd ..

echo "export fd_dev=nvme1n1" >> ~/.profile
echo 'export sd_dev=nvme0n1' >> ~/.profile
